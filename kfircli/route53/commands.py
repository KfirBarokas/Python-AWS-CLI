from kfircli.route53 import operations

from kfircli.common.consts import ROUTE53_ZONE_TYPE_PUBLIC, ROUTE53_ZONE_TYPES, VPC_ID


def register_route53_commands(subparsers):
    parser = subparsers.add_parser("route53", help="AWS Route 53")
    route53_subparsers = parser.add_subparsers(
        dest="action", title="action", description="Available Route 53 actions"
    )

    # create zone
    create_zone = route53_subparsers.add_parser("create-zone", help="Create a DNS Zone")
    create_zone.add_argument("--name", required=True, help="Zone name")
    create_zone.add_argument(
        "--type",
        default=ROUTE53_ZONE_TYPE_PUBLIC,
        help="public - route traffic on internet, private - route traffic within a VPC",
        choices=ROUTE53_ZONE_TYPES,
    )
    create_zone.add_argument(
        "--vpc-region",
        help="For PRIVATE, region of VPC",
        choices=["us-east-1"],
        default="us-east-1",
    )
    create_zone.add_argument(
        "--vpc-id", help="For PRIVATE, ID of VPC", choices=[VPC_ID], default=VPC_ID
    )
    create_zone.set_defaults(func=operations.create_zone_cli)

    # create record
    create_record = route53_subparsers.add_parser(
        "create-record", help="Create a DNS Record"
    )
    create_record.add_argument("--zone-id", required=True, help="Zone id")
    create_record.add_argument("--record-name", required=True, help="Record name")
    create_record.add_argument(
        "--record-type",
        required=True,
        help="Record type (A | AAAA | CAA | CNAME | DS | MX | NAPTR | NS | PTR | SOA | SPF | SRV)",
    )
    create_record.add_argument(
        "--record-ttl", required=True, help="Record TTL (Time to live)"
    )
    create_record.add_argument(
        "--record-value", required=True, help="Record value (IP Address for example)"
    )
    create_record.set_defaults(func=operations.create_record_cli)

    # delete record
    delete_record = route53_subparsers.add_parser(
        "delete-record", help="Delete a DNS Record"
    )
    delete_record.add_argument("--zone-id", required=True, help="Zone id")
    delete_record.add_argument("--record-name", required=True, help="Record name")
    delete_record.add_argument(
        "--record-type",
        required=True,
        help="Record type (A | AAAA | CAA | CNAME | DS | MX | NAPTR | NS | PTR | SOA | SPF | SRV)",
    )
    delete_record.add_argument(
        "--record-ttl", required=True, help="Record TTL (Time to live)"
    )
    delete_record.add_argument(
        "--record-value", required=True, help="Record value (IP Address for example)"
    )
    delete_record.set_defaults(func=operations.delete_record_cli)

    # update record
    update_record = route53_subparsers.add_parser(
        "update-record", help="Update a DNS Record"
    )
    update_record.add_argument("--zone-id", required=True, help="Zone id")
    update_record.add_argument("--record-name", required=True, help="Record name")
    update_record.add_argument(
        "--record-type",
        required=True,
        help="Record type (A | AAAA | CAA | CNAME | DS | MX | NAPTR | NS | PTR | SOA | SPF | SRV)",
    )
    update_record.add_argument(
        "--record-ttl", required=True, help="Record TTL (Time to live)"
    )
    update_record.add_argument(
        "--record-value", required=True, help="Record value (IP Address for example)"
    )
    update_record.set_defaults(func=operations.update_record_cli)

    # list
    list_zones = route53_subparsers.add_parser("list", help="List zones and records")
    list_zones.set_defaults(func=operations.list_zones_cli)
