from django.core.management.base import (
    BaseCommand,
)

from assets.models import (
    Relationship,
)

from organizations.models import (
    Organization,
)

from security.models import (
    SecurityControl,
    Vulnerability,
)


class Command(BaseCommand):
    help = (
        "Seed repeatable RiftTrace "
        "Phase 11 security controls."
    )


    def handle(
        self,
        *args,
        **options,
    ):
        organization = (
            Organization.objects.get(
                name="RiftTrace Labs"
            )
        )


        def relationship(
            source_name,
            target_name,
        ):
            result = (
                Relationship.objects
                .filter(
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
                .order_by("id")
                .first()
            )


            if result is None:
                raise RuntimeError(
                    "Missing relationship: "
                    f"{source_name}"
                    " -> "
                    f"{target_name}"
                )


            return result


        def vulnerability(
            reference_id,
        ):
            result = (
                Vulnerability.objects
                .filter(
                    asset__organization=(
                        organization
                    ),

                    reference_id=(
                        reference_id
                    ),
                )
                .first()
            )


            if result is None:
                raise RuntimeError(
                    "Missing vulnerability: "
                    f"{reference_id}"
                )


            return result


        web_to_api = relationship(
            "Public Web App",
            "Internal API",
        )


        api_to_database = relationship(
            "Internal API",
            "Customer Database",
        )


        vpn_to_admin = relationship(
            "VPN Gateway",
            "Admin Workstation",
        )


        admin_to_dc = relationship(
            "Admin Workstation",
            "Domain Controller",
        )


        api_vulnerability = vulnerability(
            "DEMO-RT-API-001"
        )


        controls = [
            {
                "name":
                    "Segment Web from Internal API",

                "control_type":
                    SecurityControl
                    .ControlType
                    .NETWORK_SEGMENTATION,

                "target_relationship":
                    web_to_api,

                "target_vulnerability":
                    None,

                "description":
                    (
                        "Temporarily model "
                        "network segmentation "
                        "between the public web "
                        "application and internal "
                        "API."
                    ),
            },

            {
                "name":
                    "Patch Internal API Weakness",

                "control_type":
                    SecurityControl
                    .ControlType
                    .VULNERABILITY_REMEDIATION,

                "target_relationship":
                    None,

                "target_vulnerability":
                    api_vulnerability,

                "description":
                    (
                        "Temporarily model "
                        "remediation of the "
                        "Internal API weakness."
                    ),
            },

            {
                "name":
                    "Require MFA for VPN Admin Access",

                "control_type":
                    SecurityControl
                    .ControlType
                    .MFA,

                "target_relationship":
                    vpn_to_admin,

                "target_vulnerability":
                    None,

                "description":
                    (
                        "Temporarily require MFA "
                        "for the modeled VPN to "
                        "Admin Workstation path."
                    ),
            },

            {
                "name":
                    "Apply Least Privilege to Admin DC Access",

                "control_type":
                    SecurityControl
                    .ControlType
                    .LEAST_PRIVILEGE,

                "target_relationship":
                    admin_to_dc,

                "target_vulnerability":
                    None,

                "description":
                    (
                        "Temporarily require "
                        "HIGH source privilege "
                        "for Admin Workstation "
                        "access to the Domain "
                        "Controller."
                    ),
            },

            {
                "name":
                    "Enforce Authentication for Database Access",

                "control_type":
                    SecurityControl
                    .ControlType
                    .AUTHENTICATION_ENFORCEMENT,

                "target_relationship":
                    api_to_database,

                "target_vulnerability":
                    None,

                "description":
                    (
                        "Temporarily require "
                        "authentication for "
                        "Internal API access to "
                        "the Customer Database."
                    ),
            },
        ]


        for definition in controls:
            (
                SecurityControl.objects
                .update_or_create(
                    organization=(
                        organization
                    ),

                    name=definition[
                        "name"
                    ],

                    defaults={
                        "control_type":
                            definition[
                                "control_type"
                            ],

                        "target_relationship":
                            definition[
                                "target_relationship"
                            ],

                        "target_vulnerability":
                            definition[
                                "target_vulnerability"
                            ],

                        "description":
                            definition[
                                "description"
                            ],
                    },
                )
            )


        self.stdout.write(
            self.style.SUCCESS(
                "Phase 11 security controls "
                "are ready."
            )
        )
