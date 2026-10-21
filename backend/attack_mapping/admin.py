from django.contrib import admin

from .models import (
    AttackMappingRule,
    AttackTechnique,
)


@admin.register(AttackTechnique)
class AttackTechniqueAdmin(
    admin.ModelAdmin
):
    list_display = (
        "attack_id",
        "name",
        "domain",
        "source_version",
        "enabled",
    )

    list_filter = (
        "domain",
        "source_version",
        "enabled",
    )

    search_fields = (
        "attack_id",
        "name",
    )


@admin.register(AttackMappingRule)
class AttackMappingRuleAdmin(
    admin.ModelAdmin
):
    list_display = (
        "rule_code",
        "event_type",
        "technique",
        "priority",
        "enabled",
    )

    list_filter = (
        "event_type",
        "enabled",
    )

    search_fields = (
        "rule_code",
        "name",
        "technique__attack_id",
        "technique__name",
    )
