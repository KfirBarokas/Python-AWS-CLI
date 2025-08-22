# create - private/public
# if public - request confirmation (yes/no)
# add tags

# upload to bucket - id, path to file

# list all buckets
import boto3
from common.consts import RESOURCE_DEFAULT_TAGS
import json

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


def create_bucket_with_tags(name, tags, block_public):
    s3_client.create_bucket(Bucket=name)
    s3_client.put_bucket_tagging(Bucket=name, Tagging={"TagSet": tags})

    if not block_public:
        set_bucket_public(name)


create_bucket_with_tags("kfir-test123123", RESOURCE_DEFAULT_TAGS, False)
