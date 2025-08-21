import boto3
from botocore.exceptions import ClientError

from tabulate import tabulate
from ec2.errors import *
from operator import itemgetter


# Create a single resource + client so functions can reuse them
ec2_resource = boto3.resource("ec2")
ec2_client = boto3.client("ec2")

MAX_RUNNING_INSTANCES = 2

AVAILABLE_INSTANCE_TYPES = ["t3.micro", "t2.small"]
AVAILABLE_IMAGES = ["amazon", "ubuntu"]

CANOICAL_OWNER_ID = "099720109477"
UBUNTU_NAME_PATTERN = "ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-*-*"

AMAZON_LINUX_NAME_PATTERN = "al2023-ami-*-x86_64"

INSTANCE_STATE_RUNNING = "running"
INSTANCE_STATE_STOPPED = "stopped"


def create_instance(
    image_id, instance_type, key_name, sec_group_ids: list, subnet_id, tags: list = None
):

    if get_running_instance_count_by_tags(tags) >= MAX_RUNNING_INSTANCES:
        raise RunningInstanceCountLimitReached(MAX_RUNNING_INSTANCES)

    if instance_type not in AVAILABLE_INSTANCE_TYPES:
        raise InstanceTypeError(AVAILABLE_INSTANCE_TYPES)

    tag_spec = []
    if tags:
        tag_spec = [{"ResourceType": "instance", "Tags": tags}]

    client = boto3.client("ec2")

    try:
        instances = ec2_resource.create_instances(
            ImageId=image_id,
            InstanceType=instance_type,
            KeyName=key_name,
            SecurityGroupIds=sec_group_ids,
            SubnetId=subnet_id,
            MinCount=1,
            MaxCount=1,
            TagSpecifications=tag_spec,
        )
    except Exception as e:
        raise InstanceCreateError(str(e))

    return instances[0]  # return first instance object


def check_instance_exists(instance_id):
    instance = ec2_resource.Instance(instance_id)
    try:
        instance.load()
        return True
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code in ("InvalidInstanceID.NotFound", "InvalidInstanceID.Malformed"):
            return False
        raise  # re-raise unexpected errors


def start_instance_with_tags(instance_id, tags):
    if check_instance_exists(instance_id) == False:
        raise NoInstanceFoundById(instance_id)

    if get_running_instance_count_by_tags(tags) >= MAX_RUNNING_INSTANCES:
        raise RunningInstanceCountLimitReached(MAX_RUNNING_INSTANCES)

    if instance.state["Name"] == INSTANCE_STATE_RUNNING:
        raise InstanceAlreadyInState(INSTANCE_STATE_RUNNING)

    instance = ec2_resource.Instance(instance_id)
    instance.start()
    instance.wait_until_running()
    return instance.state


def stop_instance_with_tags(instance_id, tags):
    if check_instance_exists(instance_id) == False:
        raise NoInstanceFoundById(instance_id)

    if get_running_instance_count_by_tags(tags) == 0:
        raise NoRunningInstancesError

    if instance.state["Name"] == INSTANCE_STATE_STOPPED:
        raise InstanceAlreadyInState(INSTANCE_STATE_STOPPED)

    instance = ec2_resource.Instance(instance_id)
    instance.stop()
    instance.wait_until_stopped()
    return instance.state


def terminate_instance(instance_id):
    # TODO complete this
    """Terminate an EC2 instance"""
    instance = ec2_resource.Instance(instance_id)
    instance.terminate()
    instance.wait_until_terminated()
    return instance.state


def instance_has_tag(instance_tags, tag):
    for instance_tag in instance_tags:
        if instance_tag["Key"] == tag["Key"] and instance_tag["Value"] == tag["Value"]:
            return True
    return False


def instance_tags_match_tags(instance_tags, tags_to_match):
    for tag in tags_to_match:
        if not instance_has_tag(instance_tags, tag):
            return False
    return True


def list_instances_by_tags(tags):
    instances = []
    response = ec2_client.describe_instances()

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:

            if instance_tags_match_tags(instance["Tags"], tags):
                instance_id = instance["InstanceId"]
                instance_type = instance["InstanceType"]
                instance_state = instance["State"]["Name"]

                instance_public_ip = instance.get("PublicIpAddress", "N/A")
                instances.append(
                    {
                        "instance_id": instance_id,
                        "instance_type": instance_type,
                        "instance_state": instance_state,
                        "instance_public_ip": instance_public_ip,
                    }
                )

    return instances


def print_instances_table(instances):
    if not instances:
        print("No instances found.")
        return

    table_data = []
    for instance in instances:
        table_data.append(
            [
                instance["instance_id"],
                instance["instance_type"],
                instance["instance_state"],
                instance["instance_public_ip"],
            ]
        )

    headers = ["ID", "Type", "State", "Public IP"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))


def get_running_instance_count_by_tags(tags):
    instances = list_instances_by_tags(tags)
    running_instances_count = 0

    for instance in instances:
        if instance["instance_state"] == INSTANCE_STATE_RUNNING:
            running_instances_count += 1

    return running_instances_count


def choose_and_get_latest_ami_id(image_os_name):
    if image_os_name not in AVAILABLE_IMAGES:
        raise AMITypeError(AVAILABLE_IMAGES)

    if image_os_name == "amazon":
        return get_latest_ami_id("amazon", AMAZON_LINUX_NAME_PATTERN)

    if image_os_name == "ubuntu":
        return get_latest_ami_id(CANOICAL_OWNER_ID, UBUNTU_NAME_PATTERN)


def get_latest_ami_id(owner, name_pattern):
    print("Getting latest AMI...")
    response = ec2_client.describe_images(
        Filters=[
            {
                "Name": "name",
                "Values": [name_pattern],
            },
            {"Name": "state", "Values": ["available"]},
            {"Name": "free-tier-eligible", "Values": ["true"]},
        ],
        Owners=[owner],
    )
    image_details = sorted(
        response["Images"], key=itemgetter("CreationDate"), reverse=True
    )
    ami_id = image_details[0]["ImageId"]
    print(ami_id)
    return ami_id
