from common.consts import (
    AVAILABLE_IMAGES,
    AVAILABLE_INSTANCE_TYPES,
    EC2_DEFAULT_SECURITY_GROUP_ID,
    EC2_DEFAULT_SUBNET_ID,
)

from . import operations


def register_ec2_commands(subparsers):
    parser = subparsers.add_parser("ec2", help="AWS EC2 Instance")
    ec2_subparsers = parser.add_subparsers(
        dest="action", title="action", description="Available EC2 actions"
    )

    # create
    create = ec2_subparsers.add_parser("create", help="Create an ec2 instance")
    create.add_argument(
        "--ami", required=True, help="AMI Name", choices=AVAILABLE_IMAGES
    )
    create.add_argument(
        "--type",
        default="t3.micro",
        help="Instance type",
        choices=AVAILABLE_INSTANCE_TYPES,
    )
    create.add_argument("--key-name", required=True, help="Name of SSH key", type=str)
    create.add_argument(
        "--security-group-id",
        default=EC2_DEFAULT_SECURITY_GROUP_ID,
        help="ID of security group",
    )
    create.add_argument(
        "--subnet-id", default=EC2_DEFAULT_SUBNET_ID, help="ID of subnet"
    )

    create.set_defaults(func=operations.create_instance_cli)

    # list
    list_cli = ec2_subparsers.add_parser("list", help="List ec2 instances")
    list_cli.set_defaults(func=operations.list_instances_cli)
