import argparse
import boto3
import datetime
import time
import os
from tqdm import tqdm, trange
import numpy as np

from AWS.S3.randomly_select_files import get_s3_directories, copy_path_to_different_bucket, create_full_bucket_paths

import logging
# FORMAT = "[%(asctime)s][%(levelname)s][%(pathname)s][%(funcName)s] %(message)s"
# logging.basicConfig(level=logging.INFO, format=FORMAT)
logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="randomly select files from S3 bucket", fromfile_prefix_chars="@")

    parser.add_argument('--source-bucket', type=str,
                        required=True,
                        help='S3 source bucket name')

    parser.add_argument('--source-path', type=str,
                        help='prefix of all files in bucket')

    parser.add_argument('--dest-bucket', type=str,
                        required=True,
                        help='S3 destination bucket name (files will be copied here)')

    parser.add_argument('--filter', type=str, nargs='+',
                        help='files will contain this string')

    parser.add_argument('--from-date', type=str,
                        help='select files from folder with time stamp later than this date')
    args, unknown_args = parser.parse_known_args()

    # create connection
    s3 = boto3.client("s3")

    # get bucket
    try:
        bucket_head = s3.head_bucket(Bucket=args.source_bucket)
        logging.info("connected to bucket: {}".format(args.source_bucket))

    except Exception:
        logging.error("{} bucket does not exist".format(args.source_bucket))

    paginator = s3.get_paginator("list_objects")
    page_iterator = paginator.paginate(Bucket=args.source_bucket, Prefix=args.source_path)
    # all_folders = get_s3_directories(s3, args.source_bucket, prefix=args.source_path)[0]
    # iterating over all bucket data
    batch = 0
    for page in page_iterator:
        batch += 1
        objects = page["Contents"]

        # filtering files if required
        valid_files = [f["Key"] for f in objects]
        for filt in args.filter:
            valid_files = [f for f in valid_files if filt in f]

        if args.from_date:
            t0 = time.mktime(datetime.datetime.strptime(args.from_date, "%Y-%m-%d").timetuple())
            valid_files = [f for f in valid_files if
                           time.mktime(datetime.datetime.strptime(f.split("/")[1].split("_")[0], "%Y-%m-%d").timetuple()) > t0]


        # logging.info("copying {} files from {} to {}".format(len(all_files), args.source_bucket, args.dest_bucket))
        # copy_path_to_different_bucket(s3, args.source_bucket_name, sampled_rgb_paths, args.dest_bucket_name)
        logging.info("batch {} ,copying files {}".format(batch, len(valid_files)))
        pbar = tqdm(valid_files, desc="copying files {}".format(len(valid_files)), position=0, leave=True)
        for key in pbar:
            copy_source = {"Bucket": args.source_bucket, "Key": key}
            success = s3.copy_object(CopySource=copy_source, Bucket=args.dest_bucket, Key=key)
            pbar.set_postfix(copying=key)
            pbar.update()

    logging.info("done...")

    logging.info(10 * "=" + " finished " + 10 * "=")


if __name__ == "__main__":
    main()