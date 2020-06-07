import dtlpy as dl
import os
import argparse
from DataLoop import establish_dataloop_connection
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger(__name__)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="convert_annotations_to_YOLO_and_download", fromfile_prefix_chars="@")

    parser.add_argument('--project-name', type=str, default="Elbit",
                        required=True,
                        help='path to annoations on dataloop server')

    parser.add_argument('--dataloop-path', type=str,
                        required=True,
                        help='path to annoations on dataloop server')

    parser.add_argument('--local-dest', type=str,
                        required=True,
                        help='local path where annoations will be saved')

    args = parser.parse_args()
    print(args)
    # connect to dataloop server
    establish_dataloop_connection(args)

    # upload the entire local input folder to dest location on dataloop server
    project = dl.projects.get(project_name=args.project_name)


    try:
        dataset = project.datasets.get(dataset_name=args.dataloop_path)
        logging.info("dataset {} found".format(args.dataloop_path))

    except Exception:
        dataset = project.datasets.create(dataset_name=args.dest_dataloop_path)
        logging.info("successfully created new dataset with following name: {}".format(args.dest_dataloop_path))

    # downloading images
    dataset.items.download(local_path=args.local_dest, annotation_options='box')

    # converting to yolo and downloading
    converter = dl.Converter()
    filters = dl.Filters()
    # filtering only boxes
    filters.resource = dl.FiltersResource.ANNOTATION
    filters.add(field='type', values='box')

    # downloading labels and converting
    converter.convert_dataset(dataset=dataset,
                              to_format='yolo',
                              local_path=args.local_dest,
                              annotation_filter=filters)
