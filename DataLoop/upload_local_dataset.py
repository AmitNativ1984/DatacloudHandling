import dtlpy as dl
import os
import argparse
from DataLoop import establish_dataloop_connection
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger(__name__)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="upload local folder and subfolders to dataloop", fromfile_prefix_chars="@")

    parser.add_argument('--source', type=str,
                        required=True,
                        help='local path')

    parser.add_argument('--dest-dataloop-path', type=str,
                        required=True,
                        help='dest path inside dataloop project')

    args = parser.parse_args()
    print(args)
    # connect to dataloop server
    establish_dataloop_connection()

    # upload the entire local input folder to dest location on dataloop server
    project = dl.projects.get(project_name="Elbit")
    new_dataset = project.datasets.create(dataset_name=args.dest_dataloop_path)
    logging.info("successfully created following path on dataloop folder: {}".format(args.dest_dataloop_path))

    # go down tree of local dataset and upload all files. keeping tree structure
    for curr_path in os.walk(args.source):
        # check files do exist in current path
        files = curr_path[-1]
        if not files:
            continue

        remote_subfolder = curr_path[0].split(args.source)[-1]
        # upload all files in subfolder:
        new_dataset.items.upload(local_path=curr_path[0])
        logging.info("successfully updated all files from {}".format(curr_path[0]))

    logging.info("finished uploading files")
