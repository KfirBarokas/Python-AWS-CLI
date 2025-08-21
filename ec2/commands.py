from common.consts import (
    AVAILABLE_IMAGES,
    AVAILABLE_INSTANCE_TYPES,
    EC2_DEFAULT_SECURITY_GROUP_ID,
    EC2_DEFAULT_SUBNET_ID,
)


def register_ec2_commands(subparsers):
    ec2_parser = subparsers.add_parser("ec2", help="AWS EC2 Instance")
    ec2_subparsers = ec2_parser.add_subparsers(
        title="create", description="Create an ec2 instance"
    )

    # create
    ec2_create = ec2_subparsers.add_parser("create", help="Create an ec2 instance")
    ec2_create.add_argument(
        "--ami", required=True, help="AMI Name", choices=AVAILABLE_IMAGES
    )
    ec2_create.add_argument(
        "--type",
        default="t3.micro",
        help="Instance type",
        choices=AVAILABLE_INSTANCE_TYPES,
    )
    ec2_create.add_argument(
        "--key-name", required=True, help="Name of SSH key", type=str
    )
    ec2_create.add_argument(
        "--security-group-id",
        default=EC2_DEFAULT_SECURITY_GROUP_ID,
        help="ID of security group",
    )
    ec2_create.add_argument(
        "--subnet-id", default=EC2_DEFAULT_SUBNET_ID, help="ID of subnet"
    )
