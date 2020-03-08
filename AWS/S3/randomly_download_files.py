import argparse
import boto3
import datetime
import time
import os
from tqdm import tqdm
import numpy as np
import random

import logging
FORMAT = "[%(asctime)s][%(levelname)s][%(pathname)s][%(funcName)s] %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)
logging.getLogger(__name__)


def get_s3_directories(s3, bucket_name, prefix=""):
    # get list of folders subfolders inside bucket
    logging.info("retrieving s3 folders and subfolders")
    parent_folders = s3.list_objects(Bucket=bucket_name, Prefix=prefix, Delimiter="/")["CommonPrefixes"]
    for folder in parent_folders:
        try:
            folder["Children"] = [path["Prefix"].split("/")[1]
                                  for path in s3.list_objects(Bucket=bucket_name, Prefix=folder["Prefix"], Delimiter="/")[
                                      "CommonPrefixes"]]
        except Exception:
            logging.info("folder {} did not have sub folders".format(folder["Prefix"]))

    logging.info("done...")
    return parent_folders

def filter_folders_names_by_date(folders, date):
    """ return folders of experiments taken after date in <yyyy-mm-dd>"""

    valid_folders=[]
    t0 = time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple())
    logging.info("filtering all subfolders with date string prior to " + date)
    for folder in folders:
        logging.info("searching " + folder["Prefix"])
        filtered_childern = []
        for child in folder["Children"]:
            # get all experiment dates:
            time_stamp = child.split("_")[0]
            try:
                t1 = time.mktime(datetime.datetime.strptime(time_stamp, "%Y-%m-%d").timetuple())
            except Exception:
                t1 = time.mktime(datetime.datetime.strptime(time_stamp, "%d-%m-%Y").timetuple())

            if t1 >= t0:
                filtered_childern.append(child)

        folder["Children"] = filtered_childern

        logging.info("done...")

    return folders

def create_full_bucket_paths(s3, bucket_name, folders, file_prefix=None):
    """
        returns a list of all files in s3 bucket.
        s3 - s3 bucket
        folders - list of all valid paths (prefixes) in bucket
        file_prefix - list;  prefix to all rgb image files.
    """
    paths = []
    if file_prefix is None:
        file_prefix = ""

    # creating a list of all subfolders in bucket
    for folder in folders:
        parent = folder["Prefix"]
        for child in folder["Children"]:
            paths.append(os.path.join(parent, child))
            logging.info("added path {}".format(paths[-1]))

    bucket_rgb_paths = []
    pbar = tqdm(paths)
    pbar.set_description("collecting rgb images paths")
    for path in pbar:
        filenames = s3.list_objects(Bucket=bucket_name, Prefix=path + "/" + file_prefix)["Contents"]
        # rgb_path = [f["Key"] for f in filenames if ]
        bucket_rgb_paths += rgb_path

    logging.info("total of {} images found".format(len(bucket_rgb_paths)))
    return bucket_rgb_paths

def collect_matching_nightCam_Velodyne(rgb_paths, rgb_file_prefix, night_cam_prefix, velodyne_prefix):
    """ return rgb images matching night cam and velodyne  paths """

    logging.info("collecting rgb images matching night cam and velodyne paths")
    night_cam_paths = [path.replace(rgb_file_prefix[0], night_cam_prefix[0]).replace(rgb_file_prefix[1], night_cam_prefix[1])
                       for path in rgb_paths]

    velodyne_paths = [path.replace(rgb_file_prefix[0], velodyne_prefix[0]).replace(rgb_file_prefix[1], velodyne_prefix[1])
                       for path in rgb_paths]

    logging.info("done...")
    return night_cam_paths, velodyne_paths

def copy_path_to_different_bucket(s3, sourceBucket, sourcePath, destBucket, metadata=None):
    pbar = tqdm(sourcePath)
    pbar.set_description("copy files to s3 Bucket: {}".format(destBucket))
    for key in pbar:
        copy_source = {"Bucket": sourceBucket, "Key": key}
        try:
            if metadata is None:
                success = s3.copy_object(CopySource=copy_source, Bucket=destBucket, Key=key)
            else:
                success = s3.copy_object(CopySource=copy_source, Bucket=destBucket, Key=key, Metadata=metadata, MetadataDirective='REPLACE')
        except Exception:
            logging.error("cannot copy {} to Bucket: {}, Key: {}".format(sourceBucket, destBucket, key))
            continue

    return success

def main():
    parser = argparse.ArgumentParser(description="randomly download files from S3 bucket", fromfile_prefix_chars="@")

    parser.add_argument('--source-bucket', type=str,
                        required=True,
                        help='S3 source bucket name')

    parser.add_argument('--local-path', type=str,
                        required=True,
                        help='local path (files will be downloaded here)')

    parser.add_argument('--prefix', type=str, default="",
                        required=True,
                        help='prefix to filter inside source bucket')

    parser.add_argument('--delimiter', type=str, default="",
                        help='delimiter to filter inside source bucket')

    parser.add_argument('--from-date', type=str, default=None,
                        help='filter all S3 object after this date')

    parser.add_argument('--n-samples', type=int,
                        required=True,
                        help='number of samples to randomly download from source bucket to local folder')

    parser.add_argument('--common-str', type=str, default='',
                        help='common str to all filenames')

    args, unknown_args = parser.parse_known_args()

    metadata = {"tagging_status": "sent_for_tagging"}

    # create connection
    s3 = boto3.client("s3")

    # get bucket
    try:
        bucket_head = s3.head_bucket(Bucket=args.source_bucket)
        logging.info("connected to bucket: {}".format(args.source_bucket))

    except Exception:
        logging.error("{} bucket does not exist".format(args.source_bucket))

    logging.info("retrieving all file names in bucket...")

    paginator = s3.get_paginator("list_objects")
    page_iterator = paginator.paginate(Bucket=args.source_bucket, Prefix=args.prefix, Delimiter=args.delimiter)

    batch = 1
    objects_full_list = []
    pbar = tqdm(page_iterator, desc="[batch {}]".format(batch), position=0, leave=True)
    for page in pbar:


        objects = page["Contents"]

        # filtering files if required
        paths = [f["Key"] for f in objects]
        img_paths = [img_path for img_path in paths if args.common_str in img_path and (img_path.endswith('jp2') or img_path.endswith('bmp'))]

        objects_full_list += img_paths

        pbar.set_description("[batch {}]".format(batch))
        pbar.set_postfix_str("total_image_files: {}".format(len(objects_full_list)))
        pbar.update()
        batch += 1

    logging.info("done...")

    logging.info("selecting {} random objects from {}".format(args.n_samples, args.source_bucket))
    random.shuffle(objects_full_list)

    selected_objects_keys = objects_full_list[:min(len(objects_full_list), args.n_samples)]

    # downloading selected files
    # downloading all objects
    pbar = tqdm(total=len(selected_objects_keys))
    pbar.set_description("downloading files")
    for key in selected_objects_keys:
        # get object path and make sure local folders have been created
        objPath, objFile = os.path.split(key)
        localPath = os.path.join(args.local_path, objPath)

        os.makedirs(localPath, exist_ok=True)

        # download object from s3 bucket to local
        localFullPath = os.path.join(localPath, objFile)
        s3.download_file(args.source_bucket, key, localFullPath)
        s3.delete_object(Bucket=args.source_bucket, Key=key)
        pbar.set_postfix(file=os.path.join(args.source_bucket, objPath, objFile))
        pbar.update()

    logging.info("finished downloading all files")



    logging.info(10 * "=" + " finished " + 10 * "=")


if __name__ == "__main__":
    main()