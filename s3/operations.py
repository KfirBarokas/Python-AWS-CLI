# create - private/public
# if public - request confirmation (yes/no)
# add tags

# upload to bucket - id, path to file

# list all buckets
import os
from pathlib import Path
import re

import boto3
from botocore.exceptions import ClientError

from common.consts import RESOURCE_DEFAULT_TAGS, BUCKET_ACCESS_PUBLIC

from s3.errors import *

from tabulate import tabulate
import json

s3_resource = boto3.resource("s3")
s3_client = boto3.client("s3")


def set_bucket_public(bucket_name):
    s3_client.put_public_access_block(
        Bucket=bucket_name, PublicAccessBlockConfiguration={"BlockPublicPolicy": False}
    )

    # set get object policy
    bucket_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": ["s3:GetObject"],
                "Resource": f"arn:aws:s3:::{bucket_name}/*",
            }
        ],
    }

    bucket_policy = json.dumps(bucket_policy)

    s3_client.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)


def bucket_exists(name):
    bucket = s3_resource.Bucket(name)

    if bucket.creation_date:
        return True
    else:
        return False


def create_bucket_cli(args):
    create_bucket_with_tags(args.name, RESOURCE_DEFAULT_TAGS, args.access)


def create_bucket_with_tags(name, tags, access):
    if bucket_exists(name):
        raise BucketAlreadyExists(name)

    print(name)
    s3_client.create_bucket(Bucket=name)
    s3_client.put_bucket_tagging(Bucket=name, Tagging={"TagSet": tags})

    if access == BUCKET_ACCESS_PUBLIC:
        set_bucket_public(name)


def get_bucket_name_from_arn(arn):
    return arn.split(":::")[-1]


def get_buckets_with_tags():
    tag_client = boto3.client("resourcegroupstaggingapi")
    response = tag_client.get_resources(
        ResourceTypeFilters=["s3"],
        TagFilters=[
            {"Key": "Owner", "Values": ["Kfir"]},
            {"Key": "CreatedBy", "Values": ["platform-cli"]},
        ],
    )

    buckets = []
    for resource in response["ResourceTagMappingList"]:
        arn = resource["ResourceARN"]
        bucket_name = get_bucket_name_from_arn(arn)

        bucket_object = s3_resource.Bucket(bucket_name)
        bucket_creation_date = bucket_object.creation_date

        buckets.append(
            {
                "name": bucket_name,
                "creation_date": bucket_creation_date,
            }
        )

    return buckets


def bucket_has_tags(bucket_name):
    buckets_with_tags = get_buckets_with_tags()
    has_tags = False

    for bucket in buckets_with_tags:
        if bucket["name"] == bucket_name:
            has_tags = True

    return has_tags


def list_buckets_cli(args):
    print_buckets_table(get_buckets_with_tags())


def print_buckets_table(buckets):
    if not buckets:
        print("No buckets found.")
        return

    table_data = []
    for bucket in buckets:
        table_data.append(
            [
                bucket["name"],
                bucket["creation_date"],
            ]
        )

    headers = ["Name", "Creation Date"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))


def bucket_name_valid(name):
    # S3 bucket name rules:
    # - Must be between 3 and 63 characters in length
    # - Can contain only lowercase letters, numbers, hyphens, and cannot start or end with a hyphen

    pattern = re.compile(r"^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]$")

    return bool(pattern.match(name))


def upload_file_to_bucket_cli(args):
    upload_file_to_bucket(args.bucket_name, args.file, args.file_name)


def upload_file_to_bucket(bucket_name, file_name, object_name):
    if not bucket_exists(bucket_name):
        raise BucketDoesntExist(bucket_name)

    if not bucket_name_valid(bucket_name):
        raise InvalidBucketName(bucket_name)

    if not bucket_has_tags(bucket_name):
        raise BucketDoesntHaveTags()

    file_path = Path(file_name)

    if not file_path.exists():
        raise FileDoesntExist(file_name)

    if object_name is None:
        object_name = os.path.basename(file_name)

    # upload the file
    s3_client = boto3.client("s3")
    try:
        s3_client.upload_file(file_name, bucket_name, object_name)
    except ClientError as e:
        raise ErrorUploadingFileToBucket()

    print("Uploaded file!")
