from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from assets.models import Asset
from organizations.models import Organization

from identities.models import (
    CredentialExposure,
    Identity,
    IdentityAccess,
    IdentityLink,
)


class Command(BaseCommand):
    help = (
        "Create Phase 15 identity demo data "
        "for Import Demo Corp."
    )


    def add_arguments(
        self,
        parser,
    ):
        parser.add_argument(
            "--organization",

            default="Import Demo Corp",
        )


    def handle(
        self,
        *args,
        **options,
    ):
        organization_name = options[
            "organization"
        ]


        try:
            organization = (
                Organization.objects.get(
                    name=organization_name
                )
            )

        except Organization.DoesNotExist as exc:
            raise CommandError(
                (
                    "Organization does not "
                    f"exist: {organization_name}"
                )
            ) from exc


        required_asset_names = [
            "Imported Web",
            "Imported API",
            "Imported Database",
        ]


        assets = {
            asset.name:
                asset

            for asset
            in Asset.objects.filter(
                organization=organization,

                name__in=(
                    required_asset_names
                ),
            )
        }


        missing_assets = [
            name

            for name
            in required_asset_names

            if name not in assets
        ]


        if missing_assets:
            raise CommandError(
                (
                    "Phase 14 sample assets "
                    "are missing: "
                    f"{missing_assets}"
                )
            )


        web_runtime, _ = (
            Identity.objects.update_or_create(
                organization=organization,

                name="web-runtime",

                defaults={
                    "identity_type":
                        (
                            Identity
                            .IdentityType
                            .SERVICE_ACCOUNT
                        ),

                    "privilege_level":
                        (
                            Identity
                            .PrivilegeLevel
                            .LOW
                        ),

                    "enabled":
                        True,

                    "description":
                        (
                            "Service account used "
                            "by the web tier."
                        ),
                },
            )
        )


        database_admin, _ = (
            Identity.objects.update_or_create(
                organization=organization,

                name="database-admin-role",

                defaults={
                    "identity_type":
                        (
                            Identity
                            .IdentityType
                            .ROLE
                        ),

                    "privilege_level":
                        (
                            Identity
                            .PrivilegeLevel
                            .HIGH
                        ),

                    "enabled":
                        True,

                    "description":
                        (
                            "Privileged database "
                            "administration role."
                        ),
                },
            )
        )


        CredentialExposure.objects.update_or_create(
            organization=organization,

            name=(
                "Web runtime token "
                "on Imported Web"
            ),

            defaults={
                "identity":
                    web_runtime,

                "stored_on_asset":
                    assets[
                        "Imported Web"
                    ],

                "credential_type":
                    (
                        CredentialExposure
                        .CredentialType
                        .TOKEN
                    ),

                "discoverable_on_compromise":
                    True,

                "satisfies_mfa":
                    False,

                "active":
                    True,

                "description":
                    (
                        "Synthetic credential "
                        "exposure for Phase 15."
                    ),
            },
        )


        IdentityLink.objects.update_or_create(
            organization=organization,

            source_identity=web_runtime,

            target_identity=database_admin,

            link_type=(
                IdentityLink
                .LinkType
                .ASSUMES_ROLE
            ),

            defaults={
                "requires_mfa":
                    False,

                "enabled":
                    True,

                "description":
                    (
                        "The web runtime identity "
                        "can assume the database "
                        "administrator role."
                    ),
            },
        )


        IdentityAccess.objects.update_or_create(
            organization=organization,

            identity=database_admin,

            asset=assets[
                "Imported Database"
            ],

            access_type=(
                IdentityAccess
                .AccessType
                .ADMINISTER
            ),

            defaults={
                "granted_privilege":
                    (
                        Identity
                        .PrivilegeLevel
                        .HIGH
                    ),

                "requires_mfa":
                    False,

                "enabled":
                    True,

                "description":
                    (
                        "Database admin role "
                        "can administer the "
                        "database."
                    ),
            },
        )


        self.stdout.write(
            self.style.SUCCESS(
                (
                    "Phase 15 identity demo "
                    "data created."
                )
            )
        )
