import boto3

import logging
FORMAT = "[%(asctime)s][%(levelname)s][%(module)s][%(funcName)s] %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)
logging.getLogger(__name__)

def establish_connection(resource_type):
    aws_remote_connection = boto3.client(resource_type)
    logging.info("successfully connected to {}".format(resource_type))
    if resource_type == "s3":
        for bucket in aws_remote_connection.buckets.all():
            logging.info("available bucket: " + bucket.name)

    return  aws_remote_connection


