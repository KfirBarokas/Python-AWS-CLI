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
- [General information](#general-information)
- [Cleanup](#cleanup-instructions)
- [Demo](#demo-evidence-for-submission)

---

## Prerequisites
- Git
- Python 3.10+
- `pip`
- AWS account with an IAM user/role that has permissions for EC2, S3 and Route53.
- AWS credentials configured locally

Configure AWS credentials:

```bash
aws configure # Enter credentials
```
## Compatiblity
Compatible with Windows 10 & Amazon Linux 2023

MacOS - Not tested

---


## General Information

All resources created by the CLI are tagged so the tool can safely operate on its own resources.

Tags:

- `CreatedBy=platform-cli`
- `Owner=<username>` (developer requesting the resource)

These tags are set by default; pass `--owner`, `--project`, and `--env` when creating resources to customize them.


## Installation

From the repository root:

```bash
# Clone this repo
git clone https://github.com/KfirBarokas/Python-AWS-CLI.git

cd Python-AWS-CLI

python3 -m pip install .

# View commands
kfircli -h
```

---

## Instructions

The CLI format is as follows:

```bash
kfircli <resource> <action> [options]
```

General pattern examples:

```bash
# create an EC2 instance
kfircli ec2 create --ami ubuntu --type t3.micro --key-name my-key --subnet-id subnet-0123...

# list instances
kfircli ec2 list

# create a private s3 bucket
kfircli s3 create --name my-project-dev-bucket

# create a public s3 bucket (prompts for confirmation)
kfircli s3 create --name my-public-bucket --public

# create a route53 zone
kfircli route53 create-zone --name example.dev
```

Run `--help` on the top-level or any subcommand for more details:

```bash
kfircli --help
kfircli ec2 --help
kfircli s3 --help
kfircli route53 --help
```

---

## EC2 examples

**Create an EC2 instance**

```bash
kfircli ec2 create \
  --ami ubuntu \
  --type t3.micro \
  --key-name my-ssh-key \
  --security-group-id sg-0123456789abcdef0 \
  --subnet-id subnet-0abcdef1234567890 \
  --owner alice --project demo --env dev
```

**Start an instance**

```bash
kfircli ec2 start i-0123456789abcdef0
```

**Stop an instance**

```bash
kfircli ec2 stop i-0123456789abcdef0
```

**Terminate an instance**

```bash
kfircli ec2 terminate i-0123456789abcdef0
```

**List instances created by the CLI**

```bash
kfircli ec2 list
```

---

## S3 examples

**Create a private bucket**

```bash
kfircli s3 create --name my-project-dev-bucket --owner alice --project demo --env dev
```

**Create a public bucket (interactive confirmation required)**

```bash
kfircli s3 create --name my-public-bucket --public
# CLI will prompt: Are you sure? (yes/no)
```

**Upload a file to a CLI-created bucket**

```bash
kfircli s3 upload my-project-dev-bucket ./artifact.zip
```

**List CLI-created buckets**

```bash
kfircli s3 list
```

> Upload and delete operations are allowed only for buckets the CLI created (scoped by tags).

---

## Route53 examples

**Create a hosted zone**

```bash
kfircli route53 create-zone --name example.dev --owner alice
```

**Create a record (only for CLI-created zones)**

```bash
kfircli route53 record create \
  --zone-id Z123456ABCDEFG \
  --name www.example.dev \
  --type A \
  --value 1.2.3.4 \
  --ttl 300
```

**Update a record**

```bash
kfircli route53 record update --zone-id Z123... --name www.example.dev --type A --value 5.6.7.8
```

**Delete a record**

```bash
kfircli route53 record delete --zone-id Z123... --name www.example.dev --type A
```

**List CLI-created zones & records**

```bash
kfircli route53 list
```

---


## Cleanup

**EC2**

```bash
# list CLI-created instances
kfircli ec2 list

# terminate an instance
kfircli ec2 terminate <instance-id>
```

**S3**

```bash
# empty bucket and delete
aws s3 rm s3://my-bucket --recursive --profile dev
kfircli s3 delete --name my-bucket
```

**Route53**

```bash
# delete records then delete zone
kfircli route53 record delete --zone-id Z123... --name www.example.dev --type A
kfircli route53 delete-zone --zone-id Z123...
```
---

## Demo



