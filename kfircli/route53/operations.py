# record:
#   create
#   update
#   delete

# list all zones and records of each zone
import time
from tabulate import tabulate
import boto3
from botocore.exceptions import ClientError

from kfircli.route53.errors import *
from kfircli.common.consts import (
    ROUTE53_ZONE_TYPES,
    ROUTE53_ZONE_TYPE_PUBLIC,
    ROUTE53_ZONE_TYPE_PRIVATE,
    VPC_REGION,
    VPC_ID,
    RESOURCE_DEFAULT_TAGS,
)

route53_client = boto3.client("route53")


def generate_timestamp():
    return str(time.time())


def create_zone_cli(args):
    try:
        create_zone_with_tags(
            args.name,
            args.type,
            generate_timestamp(),
            args.vpc_region,
            args.vpc_id,
        )
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "InvalidDomainName":
            raise Route53InvalidDomainName(args.name)
        else:
            raise e


def create_public_zone(name, caller_reference):
    return route53_client.create_hosted_zone(
        Name=name,
        CallerReference=caller_reference,
    )


def create_private_zone(name, caller_reference, vpc_region=None, vpc_id=None):
    return route53_client.create_hosted_zone(
        Name=name,
        VPC={"VPCRegion": vpc_region, "VPCId": vpc_id},
        CallerReference=caller_reference,
    )


def add_tags_to_zone(tags, zone_id):
    route53_client.change_tags_for_resource(
        ResourceType="hostedzone",
        ResourceId=zone_id.split("/")[
            -1
        ],  # AWS returns "/hostedzone/XXXXXXXX" → need just "XXXXXXXX"
        AddTags=tags,
    )


def create_zone_with_tags(
    name, zone_type, caller_reference, vpc_region=None, vpc_id=None
):
    response = None
    if zone_type not in ROUTE53_ZONE_TYPES:
        raise Route53InvalidZoneType(zone_type)

    if zone_type == ROUTE53_ZONE_TYPE_PUBLIC:
        response = create_public_zone(name, caller_reference)
    elif zone_type == ROUTE53_ZONE_TYPE_PRIVATE:

        # both region and id are hardcoded, to make them dynamic will take some effort...
        if vpc_region != VPC_REGION:
            raise Route53InvalidVPCRegion(vpc_region)

        if vpc_id != VPC_ID:
            raise Route53InvalidVPCID(vpc_id)

        if vpc_region == None:
            raise Route53ZoneVpcRegionCannotBeNone()

        if vpc_id == None:
            raise Route53ZoneVpcIDCannotBeNone()

        response = create_private_zone(name, caller_reference, vpc_region, vpc_id)

    zone_id = response["HostedZone"]["Id"]
    add_tags_to_zone(RESOURCE_DEFAULT_TAGS, zone_id)

    print(f"Created zone with id: {zone_id}")


def request_create_record(zone_id, record_name, record_type, record_ttl, record_value):
    route53_client.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch={
            "Changes": [
                {
                    "Action": "CREATE",
                    "ResourceRecordSet": {
                        "Name": record_name,
                        "Type": record_type,
                        "TTL": record_ttl,
                        "ResourceRecords": [{"Value": record_value}],
                    },
                }
            ]
        },
    )


def request_delete_record(zone_id, record_name, record_type, record_ttl, record_value):
    route53_client.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch={
            "Changes": [
                {
                    "Action": "DELETE",
                    "ResourceRecordSet": {
                        "Name": record_name,
                        "Type": record_type,
                        "TTL": record_ttl,
                        "ResourceRecords": [{"Value": record_value}],
                    },
                }
            ]
        },
    )


def request_update_record(zone_id, record_name, record_type, record_ttl, record_value):
    route53_client.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch={
            "Changes": [
                {
                    "Action": "UPSERT",
                    "ResourceRecordSet": {
                        "Name": record_name,
                        "Type": record_type,
                        "TTL": record_ttl,
                        "ResourceRecords": [{"Value": record_value}],
                    },
                }
            ]
        },
    )


def create_record_cli(args):
    create_record(
        args.zone_id,
        args.record_name,
        args.record_type,
        args.record_ttl,
        args.record_value,
    )


def create_record(zone_id, record_name, record_type, record_ttl, record_value):
    try:
        request_create_record(
            zone_id, record_name, record_type, record_ttl, record_value
        )
    except ClientError as e:
        raise Route53ErrorCreatingRecord(e)  # just print the error to the screen

    print(f"Created record {record_name}")


def delete_record_cli(args):
    delete_record(
        args.zone_id,
        args.record_name,
        args.record_type,
        args.record_ttl,
        args.record_value,
    )


def delete_record(zone_id, record_name, record_type, record_ttl, record_value):
    try:
        request_delete_record(
            zone_id, record_name, record_type, record_ttl, record_value
        )
    except ClientError as e:
        raise Route53ErrorDeletingRecord(e)

    print(f"Deleted record {record_name}")


def update_record_cli(args):
    update_record(
        args.zone_id,
        args.record_name,
        args.record_type,
        args.record_ttl,
        args.record_value,
    )


def update_record(zone_id, record_name, record_type, record_ttl, record_value):
    try:
        request_update_record(
            zone_id, record_name, record_type, record_ttl, record_value
        )
    except ClientError as e:
        raise Route53ErrorUpdatingRecord(e)

    print(f"Updated record {record_name}")


def print_records_table(records):
    if not records:
        print("No records found.")
        return

    table_data = []
    for record in records:
        table_data.append(
            [
                record["record_name"],
                record["record_type"],
                record["record_ttl"],
                record["record_values"],
            ]
        )

    headers = ["Name", "Type", "TTL", "Value"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))


def get_records(zone_id):
    records = []
    paginator = route53_client.get_paginator("list_resource_record_sets")
    for page in paginator.paginate(HostedZoneId=zone_id):
        for rrset in page["ResourceRecordSets"]:
            name = rrset["Name"].rstrip(".")
            record_type = rrset["Type"]
            ttl = rrset.get("TTL", "-")
            values = [r["Value"] for r in rrset.get("ResourceRecords", [])]

            records.append(
                {
                    "record_name": name,
                    "record_type": record_type,
                    "record_ttl": ttl,
                    "record_values": ", ".join(values) if values else "-",
                }
            )
    return records


def strip_zone_id(zone):
    return zone["Id"].split("/")[-1]


def get_zones_with_tags(tags):
    matching_zones = []

    required_tags = {t["Key"]: t["Value"] for t in tags}

    paginator = route53_client.get_paginator("list_hosted_zones")
    for page in paginator.paginate():
        for zone in page["HostedZones"]:

            zone_id = strip_zone_id(zone)

            tags_response = route53_client.list_tags_for_resource(
                ResourceType="hostedzone", ResourceId=zone_id
            )
            resource_tags = {
                t["Key"]: t["Value"]
                for t in tags_response.get("ResourceTagSet", {}).get("Tags", [])
            }

            matches_all_tags = True
            for key, value in required_tags.items():
                if resource_tags.get(key) != value:
                    matches_all_tags = False
                    break

            if matches_all_tags:
                matching_zones.append(
                    {"Id": zone_id, "Name": zone["Name"], "Tags": resource_tags}
                )

    return matching_zones


def list_zones_cli(args):
    print_zones_with_tags()


def print_zones_with_tags():
    zones = get_zones_with_tags(RESOURCE_DEFAULT_TAGS)
    if not zones:
        print("No zones found.")
        return
    for zone in zones:
        records = get_records(zone["Id"])

        print(f"Records for ZONE: {zone['Name']}, ID: {zone['Id']}")
        print_records_table(records)
        print("")
        print("")
