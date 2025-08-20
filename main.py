import boto3
from ec2_operation import (
    create_instance,
    list_instances_by_tags,
    get_running_instance_count_by_tags,
    print_instances_table,
    choose_and_get_latest_ami_id,
    stop_instance_with_tags,
    start_instance_with_tags,
)

# Use client to query data
ec2_client = boto3.client("ec2")
response = ec2_client.describe_instances()


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


ec2_client = boto3.client("ec2")

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
stop_instance_with_tags("-09f65cc19cd128b9b", [created_by_tag, cli_owner_tag])
# print_instances_table(list_instances_by_tags([created_by_tag, cli_owner_tag]))
# print(get_running_instance_count_by_tags([created_by_tag, cli_owner_tag]))
