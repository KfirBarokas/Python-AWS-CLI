from kfircli.common.consts import BUCKET_ACCESS_PUBLIC, BUCKET_ACCESS_PRIVATE

from kfircli.s3 import operations


def register_s3_commands(subparsers):
    parser = subparsers.add_parser("s3", help="AWS S3 Bucket")
    s3_subparsers = parser.add_subparsers(
        dest="action", title="action", description="Available S3 actions"
    )

    # create
    create = s3_subparsers.add_parser("create", help="Create a S3 bucket")
    create.add_argument("--name", required=True, help="Bucket Name")
    create.add_argument(
        "--access",
        default="private",
        help="Access to bucket (block-public-access policy)",
        choices=[BUCKET_ACCESS_PUBLIC, BUCKET_ACCESS_PRIVATE],
    )

    create.set_defaults(func=operations.create_bucket_cli)

    # upload
    upload = s3_subparsers.add_parser("upload", help="Upload a file to S3 bucket")
    upload.add_argument("bucket_name", help="Name of bucket to upload to", type=str)
    upload.add_argument("file", help="Path to file", type=str)
    upload.add_argument(
        "--file-name", help="What the file will be called in bucket", type=str
    )
    upload.set_defaults(func=operations.upload_file_to_bucket_cli)

    # list
    list_buckets = s3_subparsers.add_parser("list", help="List S3 buckets")
    list_buckets.set_defaults(func=operations.list_buckets_cli)
