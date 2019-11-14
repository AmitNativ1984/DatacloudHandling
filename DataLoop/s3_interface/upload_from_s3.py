import boto3
import dtlpy as dl
import argparse
from datetime import date

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="upload s3 files to dataloop", fromfile_prefix_chars="@")

    parser.add_argument('--s3-bucket-name', type=str,
                        required=True,
                        help='S3 source bucket name from which data will be uploaded')

    parser.add_argument('--path-in-bucket', type=str,
                        required=True,
                        help='path inside bucket from which files are uploaded')

    parser.add_argument('--dest-dataloop-path', type=str,
                        required=True,
                        help='dest path inside dataloop project')

    args = parser.parse_args()

    # new dataloop dataset name:
    new_dataset_name = date.today().strftime("%m-%d-%Y")
    s3_bucket_name = args.s3_bucket_name#"dataloop-annotations"
    path_in_bucket = args.path_in_bucket#elyakim


    bucektURL = "https://" + s3_bucket_name + ".s3amazonaws.com/"
    dl_dest = args.new_dataset_name

    # connect to s3:
    s3 = boto3.client("s3")

    # get file names of all files in parent folder in bucket
    objectURLs = [bucektURL + f["Key"] for f in s3.list_objects(Bucket=s3_bucket_name, Prefix=path_in_bucket)["Contents"]]
    objectFiles = [f["Key"] for f in s3.list_objects(Bucket=s3_bucket_name, Prefix=path_in_bucket)["Contents"]]

    ''' ======== upload to dataloop ============================ '''
    # connect to dataloop:
    dl.login()
    project = dl.projects.get(project_name="Elbit")

    # create new project in dataloop, with today date:

    # get list of all datasets in project
    datasets = project.datasets
    datasets.list().print()
