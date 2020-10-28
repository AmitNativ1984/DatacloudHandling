import sys
sys.path.append("D:\DEV\DatacloudHandling")

import dtlpy as dl
import os
import argparse
from DataLoop import establish_dataloop_connection
import logging
import cv2

# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(name=__name__)
logger.setLevel(logging.INFO)

img_file_types = ['.bmp', '.jpg', '.tif', '.tiff']

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="upload local folder and subfolders to dataloop", fromfile_prefix_chars="@")

    parser.add_argument('--project-name', type=str,
                        required=True,
                        help='dataloop project')
    parser.add_argument('--source', type=str,
                        required=True,
                        help='local path')

    parser.add_argument('--dest-dataloop-path', type=str,
                        required=True,
                        help='dest path inside dataloop project')

    parser.add_argument('--sample-rate', type=int,
                        default=1,
                        help='load every N frame')

    args = parser.parse_args()
    print(args)
    # connect to dataloop server
    establish_dataloop_connection()

    # upload the entire local input folder to dest location on dataloop server
    project = dl.projects.get(project_name=args.project_name)


    try:
        dataset = project.datasets.get(dataset_name=args.dest_dataloop_path)
        print("dataset {} found".format(args.dest_dataloop_path))

    except Exception:
        dataset = project.datasets.create(dataset_name=args.dest_dataloop_path)
        print("successfully created new dataset with following name: {}".format(args.dest_dataloop_path))

    # go down tree of local dataset and upload all files. keeping tree structure
    for curr_path in os.walk(args.source):
        # check files do exist in current path
        files = curr_path[-1]
        files = [f for f in files if os.path.splitext(f)[-1] in img_file_types]
        if not files:
            continue

        remote_subfolder = curr_path[0].split(args.source)[-1]
        # upload all files in subfolder:
        files2upload = []
        for n, file in enumerate(files):
            if n % args.sample_rate != 0:
                continue
            imgpath = os.path.join(curr_path[0], file)
            files2upload += [imgpath]
            print("collected {}".format(imgpath))

        print("\n")
        dataset.items.upload(local_path=files2upload)
        print("uploaded {} files from {}".format(len(files2upload), curr_path[0]))

    print("finished uploading files")
