import json
import os
import argparse
import dtlpy as dl
from DataLoop import establish_dataloop_connection

from tqdm import tqdm

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="upload local dataset and yolo annotations")

    parser.add_argument('--project-name', type=str,
                        required=True,
                        help='dataloop project')
    parser.add_argument('--dataset-name', type=str,
                        required=True,
                        help='remote data set name')
    parser.add_argument('--images-path', type=str,
                        required=True,
                        help='remote data set name')
    parser.add_argument('--labels-path', type=str,
                        required=True,
                        help='remote data set name')
    parser.add_argument('--labels-names', type=str,
                        required=True,
                        help='remote data set name')
    
    args = parser.parse_args()
    print(args)
    establish_dataloop_connection(args)
    project = dl.projects.get(project_name=args.project_name)
    try:
        dataset = project.datasets.get(dataset_name=args.dataset_name)
        print("dataset {} found".format(args.dataset_name))

    except Exception:
        dataset = project.datasets.create(dataset_name=args.dataset_name)
        print("successfully created new dataset with following name: {}".format(args.dataset_name))


    converter = dl.Converter()
    converter.upload_local_dataset(
        from_format=dl.AnnotationFormat.YOLO,
        dataset=dataset,
        local_items_path=args.images_path,
        local_annotations_path=args.labels_path,
        local_labels_path=args.labels_names,
        )
