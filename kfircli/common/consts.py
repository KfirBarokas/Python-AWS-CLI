import boto3

user_arn = str(boto3.client("sts").get_caller_identity().get("Arn"))
username = user_arn.split("/")[-1]

created_by_tag = {"Key": "CreatedBy", "Value": "platform-cli"}
cli_owner_tag = {"Key": "Owner", "Value": f"{username}"}


RESOURCE_DEFAULT_TAGS = [created_by_tag, cli_owner_tag]

AVAILABLE_INSTANCE_TYPES = ["t3.micro", "t2.small"]

AMAZON_IMAGE_NAME = "amazon"
AMAZON_OWNER_ID = "amazon"
AMAZON_LINUX_NAME_PATTERN = "al2023-ami-*-x86_64"

UBUNTU_IMAGE_NAME = "ubuntu"
CANOICAL_OWNER_ID = "099720109477"
UBUNTU_NAME_PATTERN = "ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-*"

AVAILABLE_IMAGES = [AMAZON_IMAGE_NAME, UBUNTU_IMAGE_NAME]

EC2_DEFAULT_SECURITY_GROUP_ID = "sg-01a75c49e095edbef"
EC2_DEFAULT_SUBNET_ID = "subnet-0468e933b4fdab115"

VPC_REGION = "us-east-1"
VPC_ID = "vpc-014e64327a6883f05"

# S3
BUCKET_ACCESS_PUBLIC = "public"
BUCKET_ACCESS_PRIVATE = "private"


# Route53
ROUTE53_ZONE_TYPE_PUBLIC = "private"
ROUTE53_ZONE_TYPE_PRIVATE = "public"
ROUTE53_ZONE_TYPES = [ROUTE53_ZONE_TYPE_PUBLIC, ROUTE53_ZONE_TYPE_PRIVATE]

RECORD_DEFAULT_TTL = 300
