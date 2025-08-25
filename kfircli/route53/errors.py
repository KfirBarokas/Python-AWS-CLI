class ROUTE53Error(Exception):
    pass


class Route53InvalidZoneType(ROUTE53Error):
    def __init__(self, zone_type):
        super().__init__(f"Invalid zone type: {zone_type}")


class Route53ZoneVpcRegionCannotBeNone(ROUTE53Error):
    def __init__(self):
        super().__init__(f"Zone vpc region cannot be None")


class Route53ZoneVpcIDCannotBeNone(ROUTE53Error):
    def __init__(self):
        super().__init__(f"Zone vpc id cannot be None")


class Route53InvalidDomainName(ROUTE53Error):
    def __init__(self, name):
        super().__init__(f"Invalid domain name: {name}")


class Route53InvalidVPCRegion(ROUTE53Error):
    def __init__(self, region):
        super().__init__(f"Invalid vpc reigon: {region}")


class Route53InvalidVPCID(ROUTE53Error):
    def __init__(self, id):
        super().__init__(f"Invalid vpc id: {id}")


class Route53ErrorCreatingRecord(ROUTE53Error):
    def __init__(self, error):
        super().__init__(error)


class Route53ErrorDeletingRecord(ROUTE53Error):
    def __init__(self, error):
        super().__init__(error)


class Route53ErrorUpdatingRecord(ROUTE53Error):
    def __init__(self, error):
        super().__init__(error)
