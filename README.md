# AWS CLI

**Automating AWS resource provisioning for development teams**

A Python CLI that allows developers to manage AWS resources (EC2, S3, Route53). 



## Table of contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Instructions](#instructions)
- [EC2 examples](#ec2-examples)
- [S3 examples](#s3-examples)
- [Route53 examples](#route53-examples)
- [Tagging convention](#tagging-convention)
- [Security & best practices](#security--best-practices)
- [Cleanup](#cleanup-instructions)
- [Demo](#demo-evidence-for-submission)

---

## Prerequisites

- Python 3.10+
- `pip`
- AWS account with an IAM user/role that has permissions for EC2, S3 and Route53.
- AWS credentials configured locally

Recommended local setup:

```bash
aws configure # Enter credentials
```
---

## Installation

From the repository root:

```bash
python -m venv .venv
# mac / linux
source .venv/bin/activate
# windows
# .venv\Scripts\activate

pip install -r requirements.txt
```

---

## Instructions

The CLI format is as follows:

```bash
python commands.py <resource> <action> [options]
```

General pattern examples:

```bash
# create an EC2 instance
python commands.py ec2 create --ami ubuntu --type t3.micro --key-name my-key --subnet-id subnet-0123...

# list instances
python commands.py ec2 list

# create a private s3 bucket
python commands.py s3 create --name my-project-dev-bucket

# create a public s3 bucket (prompts for confirmation)
python commands.py s3 create --name my-public-bucket --public

# create a route53 zone
python commands.py route53 create-zone --name example.dev
```

Run `--help` on the top-level or any subcommand for more details:

```bash
python commands.py --help
python commands.py ec2 --help
python commands.py s3 --help
python commands.py route53 --help
```

---

## EC2 examples

**Create an EC2 instance**

```bash
python commands.py ec2 create \
  --ami ubuntu \
  --type t3.micro \
  --key-name my-ssh-key \
  --security-group-id sg-0123456789abcdef0 \
  --subnet-id subnet-0abcdef1234567890 \
  --owner alice --project demo --env dev
```

**Start an instance**

```bash
python commands.py ec2 start i-0123456789abcdef0
```

**Stop an instance**

```bash
python commands.py ec2 stop i-0123456789abcdef0
```

**Terminate an instance**

```bash
python commands.py ec2 terminate i-0123456789abcdef0
```

**List instances created by the CLI**

```bash
python commands.py ec2 list
```

---

## S3 examples

**Create a private bucket**

```bash
python commands.py s3 create --name my-project-dev-bucket --owner alice --project demo --env dev
```

**Create a public bucket (interactive confirmation required)**

```bash
python commands.py s3 create --name my-public-bucket --public
# CLI will prompt: Are you sure? (yes/no)
```

**Upload a file to a CLI-created bucket**

```bash
python commands.py s3 upload my-project-dev-bucket ./artifact.zip
```

**List CLI-created buckets**

```bash
python commands.py s3 list
```

> Upload and delete operations are allowed only for buckets the CLI created (scoped by tags).

---

## Route53 examples

**Create a hosted zone**

```bash
python commands.py route53 create-zone --name example.dev --owner alice
```

**Create a record (only for CLI-created zones)**

```bash
python commands.py route53 record create \
  --zone-id Z123456ABCDEFG \
  --name www.example.dev \
  --type A \
  --value 1.2.3.4 \
  --ttl 300
```

**Update a record**

```bash
python commands.py route53 record update --zone-id Z123... --name www.example.dev --type A --value 5.6.7.8
```

**Delete a record**

```bash
python commands.py route53 record delete --zone-id Z123... --name www.example.dev --type A
```

**List CLI-created zones & records**

```bash
python commands.py route53 list
```

---

## Tagging convention

All resources created by the CLI are tagged with a consistent schema so the tool can safely discover and operate on its own resources.

Example tags applied to every resource:

- `CreatedBy=platform-cli` (primary tag used for scoping)
- `Owner=<username>` (developer requesting the resource)
- `Project=<project-name>`
- `Environment=<dev|staging|prod>`

These tags are set by default; pass `--owner`, `--project`, and `--env` when creating resources to customize them.

## Cleanup

Always confirm the AWS profile/region before running destructive commands.

**EC2**

```bash
# list CLI-created instances
python commands.py ec2 list

# terminate an instance
python commands.py ec2 terminate <instance-id>
```

**S3**

```bash
# empty bucket and delete
aws s3 rm s3://my-bucket --recursive --profile dev
python commands.py s3 delete --name my-bucket
```

**Route53**

```bash
# delete records then delete zone
python commands.py route53 record delete --zone-id Z123... --name www.example.dev --type A
python commands.py route53 delete-zone --zone-id Z123...
```
---

## Demo



