import dtlpy as dl
import os
import argparse
from DataLoop import establish_dataloop_connection
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger(__name__)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="download dataloop dataset to a local folder", fromfile_prefix_chars="@")

    parser.add_argument('--datasetname', type=str,
                        required=True,
                        help='dataset in dataloop project')

    parser.add_argument('--locallocation', type=str,
                        required=True,
                        help='local path')
                        
    parser.add_argument('--annotation_options', nargs='+',
                        required=False,
                        help='annotation options, options: json,instance,mask')                    

    parser.add_argument('--project-name', type=str, default="Elbit",
                        required=False,
                        help='project name')
                        
    args = parser.parse_args()
    print(args)
    # connect to dataloop server
    establish_dataloop_connection()

    # download the entire dataset items to the local location on the PC
    project = dl.projects.get(project_name=args.project_name)
    dataset = project.datasets.get(dataset_name=args.datasetname)
    logging.info("dataset {} found".format(args.datasetname))

    dataset.items.download(local_path = args.locallocation, annotation_options = args.annotation_options)
    logging.info("successfully downloading all files to {}".format(args.locallocation))
    logging.info("annotation options type(s): {}".format(args.annotation_options))
    logging.info("finished downloading files")