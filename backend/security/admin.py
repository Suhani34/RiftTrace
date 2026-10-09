from django.contrib import admin

from .models import (
    SecurityControl,
    Vulnerability,
)


@admin.register(Vulnerability)
class VulnerabilityAdmin(
    admin.ModelAdmin
):
    list_display = (
        "title",
        "reference_id",
        "asset",
        "attack_vector",
        "privileges_required",
        "grants_privilege",
        "cvss_score",
        "is_exploitable",
	"bypasses_mfa",
    )

    list_filter = (
        "attack_vector",
        "privileges_required",
        "grants_privilege",
        "is_exploitable",
        "bypasses_authentication",
    )

    search_fields = (
        "title",
        "reference_id",
        "asset__name",
    )

@admin.register(SecurityControl)
class SecurityControlAdmin(
    admin.ModelAdmin
):
    list_display = (
        "name",
        "organization",
        "control_type",
        "target_relationship",
        "target_vulnerability",
    )

    list_filter = (
        "control_type",
        "organization",
    )

    search_fields = (
        "name",
        "description",
    )
