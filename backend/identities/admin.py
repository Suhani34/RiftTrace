from django.contrib import admin

from .models import (
    CredentialExposure,
    Identity,
    IdentityAccess,
    IdentityLink,
)


@admin.register(Identity)
class IdentityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "organization",
        "identity_type",
        "privilege_level",
        "enabled",
    )

    list_filter = (
        "organization",
        "identity_type",
        "privilege_level",
        "enabled",
    )

    search_fields = (
        "name",
        "description",
    )


@admin.register(CredentialExposure)
class CredentialExposureAdmin(
    admin.ModelAdmin
):
    list_display = (
        "name",
        "organization",
        "identity",
        "stored_on_asset",
        "credential_type",
        "satisfies_mfa",
        "active",
    )

    list_filter = (
        "organization",
        "credential_type",
        "satisfies_mfa",
        "active",
    )


@admin.register(IdentityAccess)
class IdentityAccessAdmin(
    admin.ModelAdmin
):
    list_display = (
        "identity",
        "asset",
        "access_type",
        "granted_privilege",
        "requires_mfa",
        "enabled",
    )

    list_filter = (
        "organization",
        "access_type",
        "granted_privilege",
        "requires_mfa",
        "enabled",
    )


@admin.register(IdentityLink)
class IdentityLinkAdmin(
    admin.ModelAdmin
):
    list_display = (
        "source_identity",
        "target_identity",
        "link_type",
        "requires_mfa",
        "enabled",
    )

    list_filter = (
        "organization",
        "link_type",
        "requires_mfa",
        "enabled",
    )
