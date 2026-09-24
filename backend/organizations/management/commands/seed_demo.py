from django.core.management.base import BaseCommand

from organizations.models import Organization

from assets.models import (
    Asset,
    NetworkZone,
    Relationship,
)


class Command(BaseCommand):
    help = (
        "Create or update the RiftTrace "
        "demo cyber environment."
    )

    def handle(self, *args, **options):
        organization, _ = (
            Organization.objects.update_or_create(
                name="RiftTrace Labs",
                defaults={
                    "description": (
                        "Demo enterprise environment "
                        "used for RiftTrace development "
                        "and simulation."
                    ),
                },
            )
        )

        zone_definitions = {
            "DMZ": NetworkZone.ZoneType.DMZ,
            "Internal": (
                NetworkZone.ZoneType.INTERNAL
            ),
            "Restricted": (
                NetworkZone.ZoneType.RESTRICTED
            ),
            "Management": (
                NetworkZone.ZoneType.MANAGEMENT
            ),
        }

        zones = {}

        for name, zone_type in (
            zone_definitions.items()
        ):
            zone, _ = (
                NetworkZone.objects
                .update_or_create(
                    organization=organization,
                    name=name,
                    defaults={
                        "zone_type": zone_type,
                    },
                )
            )

            zones[name] = zone

        asset_definitions = [
            {
                "name": "Public Web App",
                "asset_type":
                    Asset.AssetType.APPLICATION,
                "criticality":
                    Asset.Criticality.HIGH,
                "environment":
                    Asset.Environment.PRODUCTION,
                "network_zone": zones["DMZ"],
                "hostname":
                    "web01.rifttrace.local",
                "ip_address":
                    "10.10.10.10",
                "is_internet_exposed": True,
            },
            {
                "name": "VPN Gateway",
                "asset_type":
                    Asset.AssetType.VPN_GATEWAY,
                "criticality":
                    Asset.Criticality.HIGH,
                "environment":
                    Asset.Environment.PRODUCTION,
                "network_zone": zones["DMZ"],
                "hostname":
                    "vpn01.rifttrace.local",
                "ip_address":
                    "10.10.10.20",
                "is_internet_exposed": True,
            },
            {
                "name": "Internal API",
                "asset_type":
                    Asset.AssetType.API,
                "criticality":
                    Asset.Criticality.HIGH,
                "environment":
                    Asset.Environment.PRODUCTION,
                "network_zone":
                    zones["Internal"],
                "hostname":
                    "api01.rifttrace.local",
                "ip_address":
                    "10.10.20.10",
                "is_internet_exposed": False,
            },
            {
                "name": "Customer Database",
                "asset_type":
                    Asset.AssetType.DATABASE,
                "criticality":
                    Asset.Criticality.CRITICAL,
                "environment":
                    Asset.Environment.PRODUCTION,
                "network_zone":
                    zones["Restricted"],
                "hostname":
                    "db01.rifttrace.local",
                "ip_address":
                    "10.10.30.10",
                "is_internet_exposed": False,
            },
            {
                "name": "File Server",
                "asset_type":
                    Asset.AssetType.FILE_SERVER,
                "criticality":
                    Asset.Criticality.HIGH,
                "environment":
                    Asset.Environment.PRODUCTION,
                "network_zone":
                    zones["Internal"],
                "hostname":
                    "files01.rifttrace.local",
                "ip_address":
                    "10.10.20.20",
                "is_internet_exposed": False,
            },
            {
                "name": "Admin Workstation",
                "asset_type":
                    Asset.AssetType.WORKSTATION,
                "criticality":
                    Asset.Criticality.HIGH,
                "environment":
                    Asset.Environment.PRODUCTION,
                "network_zone":
                    zones["Management"],
                "hostname":
                    "admin01.rifttrace.local",
                "ip_address":
                    "10.10.40.10",
                "is_internet_exposed": False,
            },
            {
                "name": "Domain Controller",
                "asset_type":
                    Asset.AssetType.DOMAIN_CONTROLLER,
                "criticality":
                    Asset.Criticality.CRITICAL,
                "environment":
                    Asset.Environment.PRODUCTION,
                "network_zone":
                    zones["Management"],
                "hostname":
                    "dc01.rifttrace.local",
                "ip_address":
                    "10.10.40.20",
                "is_internet_exposed": False,
            },
            {
                "name": "CI/CD Server",
                "asset_type":
                    Asset.AssetType.CI_CD,
                "criticality":
                    Asset.Criticality.HIGH,
                "environment":
                    Asset.Environment.PRODUCTION,
                "network_zone":
                    zones["Internal"],
                "hostname":
                    "cicd01.rifttrace.local",
                "ip_address":
                    "10.10.20.30",
                "is_internet_exposed": False,
            },
            {
                "name": "Git Repository Server",
                "asset_type":
                    Asset.AssetType.SERVER,
                "criticality":
                    Asset.Criticality.HIGH,
                "environment":
                    Asset.Environment.PRODUCTION,
                "network_zone":
                    zones["Internal"],
                "hostname":
                    "git01.rifttrace.local",
                "ip_address":
                    "10.10.20.40",
                "is_internet_exposed": False,
            },
            {
                "name": "Finance Server",
                "asset_type":
                    Asset.AssetType.SERVER,
                "criticality":
                    Asset.Criticality.CRITICAL,
                "environment":
                    Asset.Environment.PRODUCTION,
                "network_zone":
                    zones["Restricted"],
                "hostname":
                    "finance01.rifttrace.local",
                "ip_address":
                    "10.10.30.20",
                "is_internet_exposed": False,
            },
            {
                "name": "Staging Web App",
                "asset_type":
                    Asset.AssetType.APPLICATION,
                "criticality":
                    Asset.Criticality.MEDIUM,
                "environment":
                    Asset.Environment.STAGING,
                "network_zone": zones["DMZ"],
                "hostname":
                    "staging-web.rifttrace.local",
                "ip_address":
                    "10.10.10.30",
                "is_internet_exposed": False,
            },
        ]

        assets = {}

        for definition in asset_definitions:
            name = definition.pop("name")

            asset, _ = (
                Asset.objects.update_or_create(
                    organization=organization,
                    name=name,
                    defaults=definition,
                )
            )

            assets[name] = asset

        relationship_definitions = [
            (
                "Public Web App",
                "Internal API",
                Relationship.RelationshipType.CALLS,
                "HTTPS",
                443,
                True,
            ),
            (
                "Internal API",
                "Customer Database",
                Relationship.RelationshipType.READS,
                "TCP",
                5432,
                True,
            ),
            (
                "VPN Gateway",
                "Admin Workstation",
                Relationship.RelationshipType.CONNECTS_TO,
                "VPN",
                None,
                True,
            ),
            (
                "Admin Workstation",
                "Domain Controller",
                Relationship.RelationshipType.AUTHENTICATES_TO,
                "KERBEROS",
                88,
                True,
            ),
            (
                "Admin Workstation",
                "File Server",
                Relationship.RelationshipType.CONNECTS_TO,
                "SMB",
                445,
                True,
            ),
            (
                "CI/CD Server",
                "Git Repository Server",
                Relationship.RelationshipType.READS,
                "HTTPS",
                443,
                True,
            ),
            (
                "CI/CD Server",
                "Public Web App",
                Relationship.RelationshipType.WRITES,
                "HTTPS",
                443,
                True,
            ),
            (
                "Finance Server",
                "Customer Database",
                Relationship.RelationshipType.READS,
                "TCP",
                5432,
                True,
            ),
            (
                "Staging Web App",
                "Internal API",
                Relationship.RelationshipType.CALLS,
                "HTTPS",
                443,
                True,
            ),
        ]

        for (
            source_name,
            target_name,
            relationship_type,
            protocol,
            port,
            requires_authentication,
        ) in relationship_definitions:
            Relationship.objects.update_or_create(
                source=assets[source_name],
                target=assets[target_name],
                relationship_type=relationship_type,
                defaults={
                    "protocol": protocol,
                    "port": port,
                    "requires_authentication":
                        requires_authentication,
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                "RiftTrace demo environment is ready."
            )
        )
