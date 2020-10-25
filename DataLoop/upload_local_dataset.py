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

    parser.add_argument('--n', type=int, default=1, help='take only 1 every <n> files')
    parser.add_argument('--prefix', type=str, default='', help='string in file prefix')
    parser.add_argument('--postfix', type=str, default='.bmp', help='string in file end')
    parser.add_argument('--project-name', type=str, default='Elbit', help='dataloop project name')

    args = parser.parse_args()
    print(args)
    # connect to dataloop server
    establish_dataloop_connection(args)

    # upload the entire local input folder to dest location on dataloop server
    project = dl.projects.get(project_name=args.project_name)


    try:
        dataset = project.datasets.get(dataset_name=args.dest_dataloop_path)
        logging.info("dataset {} found".format(args.dest_dataloop_path))

    except Exception:
        dataset = project.datasets.create(dataset_name=args.dest_dataloop_path)
        logging.info("successfully created new dataset with following name: {}".format(args.dest_dataloop_path))

    # go down tree of local dataset and upload all files. keeping tree structure
    for path_ind, curr_path in enumerate(os.walk(args.source)):
        # check files do exist in current path
        files = curr_path[-1]
        if not files:
            continue

        for n, file in enumerate(files):
            if n % args.n != 0:
                continue

            if args.prefix not in file or args.postfix not in file:
                continue

            # upload all files in subfolder:
            dataset.items.upload(local_path=os.path.join(curr_path[0], file))
            logging.info("successfully updated all files from {}".format(curr_path[0]))

    logging.info("finished uploading files")
