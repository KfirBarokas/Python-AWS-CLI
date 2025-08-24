created_by_tag = {"Key": "CreatedBy", "Value": "platform-cli"}
cli_owner_tag = {"Key": "Owner", "Value": "kfir"}

RESOURCE_DEFAULT_TAGS = [created_by_tag, cli_owner_tag]

AVAILABLE_INSTANCE_TYPES = ["t3.micro", "t2.small"]

AMAZON_IMAGE_NAME = "amazon"
AMAZON_OWNER_ID = "amazon"
AMAZON_LINUX_NAME_PATTERN = "al2023-ami-*-x86_64"

UBUNTU_IMAGE_NAME = "ubuntu"
CANOICAL_OWNER_ID = "099720109477"
UBUNTU_NAME_PATTERN = "ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-*-*"

AVAILABLE_IMAGES = [AMAZON_IMAGE_NAME, UBUNTU_IMAGE_NAME]

EC2_DEFAULT_SECURITY_GROUP_ID = "sg-01a75c49e095edbef"
EC2_DEFAULT_SUBNET_ID = "subnet-0468e933b4fdab115"


# S3
BUCKET_ACCESS_PUBLIC = "public"
BUCKET_ACCESS_PRIVATE = "private"
