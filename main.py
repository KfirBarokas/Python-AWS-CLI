import argparse
import boto3

from ec2.commands import register_ec2_commands

# Use client to query data
# ec2_client = boto3.client("ec2")
# response = ec2_client.describe_instances()


# Use resource to manipulate objects

# File to hold predefined tags
# Helper functions to operate on a resource
EC2_IMAGE_ID = "ami-00ca32bbc84273381"
EC2_INSTANCE_TYPE = "t3.micro"
EC2_KEY_NAME = "kfir-key"
EC2_SECURITY_GROUP_IDS = ["sg-01a75c49e095edbef"]
EC2_SUBNET_ID = "subnet-0468e933b4fdab115"

created_by_tag = {"Key": "CreatedBy", "Value": "platform-cli"}
cli_owner_tag = {"Key": "Owner", "Value": "kfir"}

# print(
#     create_instance(
#         choose_and_get_latest_ami_id("amazon"),
#         EC2_INSTANCE_TYPE,
#         EC2_KEY_NAME,
#         EC2_SECURITY_GROUP_IDS,
#         EC2_SUBNET_ID,
#         [created_by_tag, cli_owner_tag],
#     )
# )
# stop_instance_with_tags("-09f65cc19cd128b9b", [created_by_tag, cli_owner_tag])
# print_instances_table(list_instances_by_tags([created_by_tag, cli_owner_tag]))
# print(get_running_instance_count_by_tags([created_by_tag, cli_owner_tag]))

# kfir-cli <resource> <action> [params]


# ec2 parameters:
# image [amazon,ubuntu]
# key-name [string]
# type [t3.micro, t2.micro]

RESOURCE_EC2 = "ec2"
RESOURCE_S3 = "s3"
RESOURCE_ROUTE53 = "route53"

EC2_RESOURCE_ACTIONS = ["create", "start", "stop", "terminate", "list"]


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(
    title="resources", description="Acceptable AWS resources"
)


def main():
    parser = argparse.ArgumentParser(prog="kfir-cli")
    subparsers = parser.add_subparsers(dest="resource")

    # Register resource subcommands
    register_ec2_commands(subparsers)
    # register_s3_commands(subparsers)
    # register_route53_commands(subparsers)

    args = parser.parse_args()
    print(args)
    print(args.type)
    print(args.ami)
    print(args.key_name)
    print(args.security_group_id)

    # if hasattr(args, "func"):
    #     args.func(args)
    # else:
    #     parser.print_help()


if __name__ == "__main__":
    main()


# terminate EC2
# start EC2
# stop EC2
# list EC2

# S3
# s3_parser = subparsers.add_parser("s3", help="AWS S3 Bucket")
