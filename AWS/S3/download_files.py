import argparse
import boto3
import datetime
import time
import os
from tqdm import tqdm
import numpy as np
from tqdm import tqdm

import logging
FORMAT = "[%(asctime)s][%(levelname)s][%(pathname)s][%(funcName)s] %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)
logging.getLogger(__name__)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="download files from bucket", fromfile_prefix_chars="@")

    parser.add_argument('--bucket', type=str,
                        required=True,
                        help='S3 source bucket name')

    parser.add_argument('--prefix', type=str,
                        required=True,
                        help='prefix of path inside bucket')

    parser.add_argument('--local-path', type=str,
                        required=True,
                        help='local path to where files will be downloaded')



    parser.add_argument('--filter', type=str,
                        help='sub string that must be part of downloaded s3 object name')

    args = parser.parse_args()

    # create connection
    s3 = boto3.client("s3")

    # get bucket
    try:
        bucket_head = s3.head_bucket(Bucket=args.bucket)
        logging.info("connected to bucket: {}".format(args.bucket))

    except Exception:
        logging.error("{} bucket does not exist".format(args.bucket))

    # get a list of all files in bucket



    objectKeys = [f["Key"] for f in s3.list_objects(Bucket=args.bucket, Prefix=args.prefix)["Contents"]]

    # downloading all objects
    pbar = tqdm(total=len(objectKeys))
    pbar.set_description("downloading files")
    for objKey in objectKeys:
        # get object path and make sure local folders have been created
        objPath, objFile =os.path.split(objKey)
        localPath = os.path.join(args.local_path, objPath)


        if args.filter is not None:
            if args.filter not in objFile:
                pbar.update()
                continue

        os.makedirs(localPath, exist_ok=True)

        # download object from s3 bucket to local
        localFullPath = os.path.join(localPath, objFile)
        s3.download_file(args.bucket, objKey, localFullPath)
        pbar.set_postfix(file=os.path.join(args.bucket, objPath, objFile))
        pbar.update()

    logging.info("finished downloading all files")