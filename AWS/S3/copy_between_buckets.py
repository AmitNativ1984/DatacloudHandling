import argparse
import boto3
import datetime
import time
import os
from tqdm import tqdm
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

    parser.add_argument('--filter', type=str,
                        help='files will contain this string')

    args, unknown_args = parser.parse_known_args()

    # create connection
    s3 = boto3.client("s3")

    # get bucket
    try:
        bucket_head = s3.head_bucket(Bucket=args.source_bucket)
        logging.info("connected to bucket: {}".format(args.source_bucket))

    except Exception:
        logging.error("{} bucket does not exist".format(args.source_bucket))

    all_files = [f["Key"] for f in s3.list_objects(Bucket=args.source_bucket, Prefix=args.source_path)["Contents"]]

    # filtering files if required
    if args.filter:
        valid_files = [f for f in all_files if args.filter in f]

    logging.info("copying {} files from {} to {}".format(len(all_files), args.source_bucket, args.dest_bucket))
    # copy_path_to_different_bucket(s3, args.source_bucket_name, sampled_rgb_paths, args.dest_bucket_name)
    pbar = tqdm(valid_files)
    pbar.set_description("copying files")
    for key in pbar:
        copy_source = {"Bucket": args.source_bucket, "Key": key}
        success = s3.copy_object(CopySource=copy_source, Bucket=args.dest_bucket, Key=key)
        pbar.set_postfix(copying=key)
        pbar.update()

    logging.info("done...")

    logging.info(10 * "=" + " finished " + 10 * "=")


if __name__ == "__main__":
    main()