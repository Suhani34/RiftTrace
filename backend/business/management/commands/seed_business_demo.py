from django.core.management.base import (
    BaseCommand,
)

from assets.models import Asset

from business.models import (
    BusinessProcess,
    BusinessProcessDependency,
)

from organizations.models import (
    Organization,
)


class Command(BaseCommand):
    help = (
        "Seed repeatable RiftTrace "
        "Phase 9 business-process data."
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
            "Domain Controller",
            "File Server",
            "CI/CD Server",
            "Git Repository Server",
            "Finance Server",
            "Staging Web App",
        }


        missing = (
            required_assets
            - set(
                assets.keys()
            )
        )


        if missing:
            raise RuntimeError(
                "Missing demo assets: "
                + ", ".join(
                    sorted(missing)
                )
            )


        process_definitions = [
            {
                "name":
                    "Customer Checkout",

                "criticality":
                    BusinessProcess
                    .Criticality
                    .CRITICAL,

                "description":
                    (
                        "Customer-facing "
                        "purchase and checkout "
                        "workflow."
                    ),

                "impact_description":
                    (
                        "Potential inability "
                        "for customers to "
                        "complete purchases."
                    ),
            },

            {
                "name":
                    "Employee Authentication",

                "criticality":
                    BusinessProcess
                    .Criticality
                    .CRITICAL,

                "description":
                    (
                        "Employee access and "
                        "identity verification."
                    ),

                "impact_description":
                    (
                        "Potential disruption "
                        "to employee access to "
                        "internal systems."
                    ),
            },

            {
                "name":
                    "Software Deployment",

                "criticality":
                    BusinessProcess
                    .Criticality
                    .HIGH,

                "description":
                    (
                        "Application build and "
                        "deployment workflow."
                    ),

                "impact_description":
                    (
                        "Potential inability "
                        "to safely release or "
                        "update software."
                    ),
            },

            {
                "name":
                    "Finance Operations",

                "criticality":
                    BusinessProcess
                    .Criticality
                    .HIGH,

                "description":
                    (
                        "Internal financial "
                        "processing workflow."
                    ),

                "impact_description":
                    (
                        "Potential disruption "
                        "to financial processing "
                        "and reporting."
                    ),
            },

            {
                "name":
                    "Internal File Collaboration",

                "criticality":
                    BusinessProcess
                    .Criticality
                    .MEDIUM,

                "description":
                    (
                        "Internal shared-file "
                        "workflow."
                    ),

                "impact_description":
                    (
                        "Potential loss of "
                        "access to shared "
                        "business files."
                    ),
            },

            {
                "name":
                    "Release Validation",

                "criticality":
                    BusinessProcess
                    .Criticality
                    .MEDIUM,

                "description":
                    (
                        "Validation of software "
                        "before production "
                        "release."
                    ),

                "impact_description":
                    (
                        "Potential disruption "
                        "to pre-release testing "
                        "and validation."
                    ),
            },
        ]


        processes = {}


        for definition in (
            process_definitions
        ):
            process, _ = (
                BusinessProcess.objects
                .update_or_create(
                    organization=organization,

                    name=definition[
                        "name"
                    ],

                    defaults={
                        "criticality":
                            definition[
                                "criticality"
                            ],

                        "description":
                            definition[
                                "description"
                            ],

                        "impact_description":
                            definition[
                                "impact_description"
                            ],
                    },
                )
            )

            processes[
                process.name
            ] = process


        dependency_definitions = [
            (
                "Customer Checkout",
                "Public Web App",
                "ESSENTIAL",
            ),

            (
                "Customer Checkout",
                "Internal API",
                "ESSENTIAL",
            ),

            (
                "Customer Checkout",
                "Customer Database",
                "ESSENTIAL",
            ),

            (
                "Employee Authentication",
                "VPN Gateway",
                "IMPORTANT",
            ),

            (
                "Employee Authentication",
                "Domain Controller",
                "ESSENTIAL",
            ),

            (
                "Software Deployment",
                "CI/CD Server",
                "ESSENTIAL",
            ),

            (
                "Software Deployment",
                "Git Repository Server",
                "ESSENTIAL",
            ),

            (
                "Software Deployment",
                "Public Web App",
                "SUPPORTING",
            ),

            (
                "Finance Operations",
                "Finance Server",
                "ESSENTIAL",
            ),

            (
                "Finance Operations",
                "Customer Database",
                "IMPORTANT",
            ),

            (
                "Internal File Collaboration",
                "File Server",
                "ESSENTIAL",
            ),

            (
                "Release Validation",
                "Staging Web App",
                "ESSENTIAL",
            ),

            (
                "Release Validation",
                "CI/CD Server",
                "IMPORTANT",
            ),
        ]


        for (
            process_name,
            asset_name,
            dependency_level,
        ) in dependency_definitions:
            (
                BusinessProcessDependency
                .objects
                .update_or_create(
                    business_process=(
                        processes[
                            process_name
                        ]
                    ),

                    asset=(
                        assets[
                            asset_name
                        ]
                    ),

                    defaults={
                        "dependency_level":
                            dependency_level,
                    },
                )
            )


        self.stdout.write(
            self.style.SUCCESS(
                "Phase 9 business demo "
                "data is ready."
            )
        )
