import dtlpy as dl
import os
import argparse
import logging
from DataLoop import establish_dataloop_connection

logging.basicConfig(level=logging.INFO)
logging.getLogger(__name__)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="convert_annotations_to_YOLO_and_download", fromfile_prefix_chars="@")

    parser.add_argument('--project-name', type=str, default="Elbit",
                        required=True,
                        help='path to annoations on dataloop server')

    parser.add_argument('--dataset-name', type=str, nargs='+',
                        required=True,
                        help='path to annoations on dataloop server')

    parser.add_argument('--local-dest', type=str,
                        required=True,
                        help='local path where annoations will be saved')

    args = parser.parse_args()
    print(args)
    # connect to dataloop server
    establish_dataloop_connection(args)


    dl.verbose.logging_level = dl.VerboseLoggingLevel.WARNING
    # upload the entire local input folder to dest location on dataloop server
    project = dl.projects.get(project_name=args.project_name)


    # downloading images
    for d, dataset_name in enumerate(args.dataset_name):
        try:
            dataset = project.datasets.get(dataset_name=dataset_name)
            logging.info("dataset {} found".format(dataset_name))

        except Exception:
            raise("dataset {} not found".format(dataset_name))

        local_dest = os.path.join(args.local_dest, dataset_name)
        dataset.items.download(local_path=local_dest, annotation_options='json')

        # converting to yolo and downloading
        converter = dl.Converter()
        filters = dl.Filters()
        # filtering only boxes
        filters.resource = dl.FiltersResource.ANNOTATION
        filters.add(field='type', values='box')

        # downloading labels and converting
        converter.convert_dataset(dataset=dataset,
                                  to_format='yolo',
                                  local_path=local_dest,
                                  annotation_filter=filters)

        os.rename(os.path.join(local_dest, "items"), os.path.join(local_dest, "images"))
        os.rename(os.path.join(local_dest, "yolo"), os.path.join(local_dest, "labels"))

        # creating data paths for train and val
        labels_path = os.path.join(local_dest, "labels")
        data_train = os.path.join(local_dest, "data_train.txt")
        data_val = os.path.join(local_dest, "data_val.txt")

        train_val_split_ratio = 0.8     # train - val ratio: 20%-80% of entire dataset

        for counter, label in enumerate(os.listdir(labels_path)):
            label_file = os.path.join(labels_path, label)
            image_file = label_file.replace('labels', 'images').replace('.txt', '.jpg')

            if os.path.isfile(image_file):

                if counter % 10 >= int(train_val_split_ratio * 10):
                    with open(data_val, 'a+') as txtfile:
                        txtfile.write(image_file + '\n')
                else:
                    with open(data_train, 'a+') as txtfile:
                        txtfile.write(image_file + '\n')
