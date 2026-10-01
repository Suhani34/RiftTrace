from django.contrib import admin

from .models import Vulnerability


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
