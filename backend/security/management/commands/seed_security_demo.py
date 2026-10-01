from django.core.management.base import (
    BaseCommand,
)

from assets.models import (
    Asset,
    Relationship,
)

from organizations.models import (
    Organization,
)

from security.models import (
    Vulnerability,
)


class Command(BaseCommand):
    help = (
        "Seed repeatable RiftTrace "
        "Phase 8 security demo data."
    )

    def handle(self, *args, **options):
        organization = (
            Organization.objects.get(
                name="RiftTrace Labs"
            )
        )

        assets = {
            asset.name: asset

            for asset
            in Asset.objects.filter(
                organization=organization
            )
        }

        required_assets = {
            "Public Web App",
            "Internal API",
            "Customer Database",
            "VPN Gateway",
            "Admin Workstation",
            "Domain Controller",
            "File Server",
            "CI/CD Server",
            "Git Repository Server",
        }

        missing = (
            required_assets
            - set(
                assets.keys()
            )
        )

        if missing:
            raise RuntimeError(
                "Missing Phase 5 demo assets: "
                + ", ".join(
                    sorted(missing)
                )
            )

        vulnerability_definitions = [
            {
                "asset":
                    assets[
                        "Internal API"
                    ],

                "reference_id":
                    "DEMO-RT-API-001",

                "title":
                    "Unauthenticated API "
                    "execution weakness",

                "cvss_score":
                    "8.1",

                "attack_vector":
                    Vulnerability
                    .AttackVector
                    .NETWORK,

                "privileges_required":
                    Vulnerability
                    .PrivilegesRequired
                    .NONE,

                "grants_privilege":
                    Vulnerability
                    .GrantedPrivilege
                    .LOW,

                "bypasses_authentication":
                    True,
            },

            {
                "asset":
                    assets[
                        "Customer Database"
                    ],

                "reference_id":
                    "DEMO-RT-DB-001",

                "title":
                    "Remote database "
                    "service weakness",

                "cvss_score":
                    "8.4",

                "attack_vector":
                    Vulnerability
                    .AttackVector
                    .NETWORK,

                "privileges_required":
                    Vulnerability
                    .PrivilegesRequired
                    .NONE,

                "grants_privilege":
                    Vulnerability
                    .GrantedPrivilege
                    .LOW,

                "bypasses_authentication":
                    True,
            },

            {
                "asset":
                    assets[
                        "Admin Workstation"
                    ],

                "reference_id":
                    "DEMO-RT-ADMIN-001",

                "title":
                    "Remote workstation "
                    "execution weakness",

                "cvss_score":
                    "8.0",

                "attack_vector":
                    Vulnerability
                    .AttackVector
                    .NETWORK,

                "privileges_required":
                    Vulnerability
                    .PrivilegesRequired
                    .NONE,

                "grants_privilege":
                    Vulnerability
                    .GrantedPrivilege
                    .LOW,

                "bypasses_authentication":
                    True,
            },

            {
                "asset":
                    assets[
                        "Admin Workstation"
                    ],

                "reference_id":
                    "DEMO-RT-ADMIN-002",

                "title":
                    "Local privilege "
                    "escalation weakness",

                "cvss_score":
                    "7.8",

                "attack_vector":
                    Vulnerability
                    .AttackVector
                    .LOCAL,

                "privileges_required":
                    Vulnerability
                    .PrivilegesRequired
                    .LOW,

                "grants_privilege":
                    Vulnerability
                    .GrantedPrivilege
                    .HIGH,

                "bypasses_authentication":
                    False,
            },

            {
                "asset":
                    assets[
                        "Domain Controller"
                    ],

                "reference_id":
                    "DEMO-RT-DC-001",

                "title":
                    "Remote domain service "
                    "weakness",

                "cvss_score":
                    "9.1",

                "attack_vector":
                    Vulnerability
                    .AttackVector
                    .NETWORK,

                "privileges_required":
                    Vulnerability
                    .PrivilegesRequired
                    .NONE,

                "grants_privilege":
                    Vulnerability
                    .GrantedPrivilege
                    .HIGH,

                "bypasses_authentication":
                    True,
            },

            {
                "asset":
                    assets[
                        "File Server"
                    ],

                "reference_id":
                    "DEMO-RT-FILE-001",

                "title":
                    "Remote file service "
                    "weakness",

                "cvss_score":
                    "7.5",

                "attack_vector":
                    Vulnerability
                    .AttackVector
                    .NETWORK,

                "privileges_required":
                    Vulnerability
                    .PrivilegesRequired
                    .NONE,

                "grants_privilege":
                    Vulnerability
                    .GrantedPrivilege
                    .LOW,

                "bypasses_authentication":
                    True,
            },

            {
                "asset":
                    assets[
                        "Git Repository Server"
                    ],

                "reference_id":
                    "DEMO-RT-GIT-001",

                "title":
                    "Repository service "
                    "remote weakness",

                "cvss_score":
                    "7.2",

                "attack_vector":
                    Vulnerability
                    .AttackVector
                    .NETWORK,

                "privileges_required":
                    Vulnerability
                    .PrivilegesRequired
                    .NONE,

                "grants_privilege":
                    Vulnerability
                    .GrantedPrivilege
                    .LOW,

                "bypasses_authentication":
                    True,
            },

            {
                "asset":
                    assets[
                        "Public Web App"
                    ],

                "reference_id":
                    "DEMO-RT-WEB-001",

                "title":
                    "Remote web execution "
                    "weakness",

                "cvss_score":
                    "8.2",

                "attack_vector":
                    Vulnerability
                    .AttackVector
                    .NETWORK,

                "privileges_required":
                    Vulnerability
                    .PrivilegesRequired
                    .NONE,

                "grants_privilege":
                    Vulnerability
                    .GrantedPrivilege
                    .LOW,

                "bypasses_authentication":
                    True,
            },
        ]

        for definition in (
            vulnerability_definitions
        ):
            (
                Vulnerability.objects
                .update_or_create(
                    asset=definition[
                        "asset"
                    ],

                    reference_id=(
                        definition[
                            "reference_id"
                        ]
                    ),

                    defaults={
                        "title":
                            definition[
                                "title"
                            ],

                        "cvss_score":
                            definition[
                                "cvss_score"
                            ],

                        "attack_vector":
                            definition[
                                "attack_vector"
                            ],

                        "privileges_required":
                            definition[
                                "privileges_required"
                            ],

                        "grants_privilege":
                            definition[
                                "grants_privilege"
                            ],

                        "bypasses_authentication":
                            definition[
                                "bypasses_authentication"
                            ],

                        "is_exploitable":
                            True,

                        "description": (
                            "Illustrative "
                            "RiftTrace Phase 8 "
                            "demo vulnerability."
                        ),
                    },
                )
            )

        def set_required_privilege(
            source_name,
            target_name,
            privilege,
        ):
            (
                Relationship.objects.filter(
                    source__organization=(
                        organization
                    ),

                    source__name=(
                        source_name
                    ),

                    target__name=(
                        target_name
                    ),
                )
                .update(
                    required_source_privilege=(
                        privilege
                    )
                )
            )

        set_required_privilege(
            "Admin Workstation",
            "Domain Controller",
            Relationship
            .RequiredSourcePrivilege
            .HIGH,
        )

        set_required_privilege(
            "Public Web App",
            "Internal API",
            Relationship
            .RequiredSourcePrivilege
            .LOW,
        )

        set_required_privilege(
            "Internal API",
            "Customer Database",
            Relationship
            .RequiredSourcePrivilege
            .LOW,
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Phase 8 security demo "
                "data is ready."
            )
        )
