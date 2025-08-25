import argparse
import sys

from kfircli.ec2.commands import register_ec2_commands
from kfircli.s3.commands import register_s3_commands
from kfircli.route53.commands import register_route53_commands

from kfircli.ec2.errors import EC2Error
from kfircli.s3.errors import S3Error
from kfircli.route53.errors import ROUTE53Error


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(
    title="resources", description="Acceptable AWS resources"
)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(prog="kfir-cli")
    subparsers = parser.add_subparsers(dest="resource")

    # Register resource subcommands
    register_ec2_commands(subparsers)
    register_s3_commands(subparsers)
    register_route53_commands(subparsers)

    args = parser.parse_args()

    if hasattr(args, "func"):
        try:
            args.func(args)
        except EC2Error as e:
            print(f"{e}")
        except S3Error as e:
            print(f"{e}")
        except ROUTE53Error as e:
            print(f"{e}")
        except Exception as e:
            print(f"{e}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
