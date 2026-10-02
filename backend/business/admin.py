from django.contrib import admin

from .models import (
    BusinessProcess,
    BusinessProcessDependency,
)


@admin.register(BusinessProcess)
class BusinessProcessAdmin(
    admin.ModelAdmin
):
    list_display = (
        "name",
        "organization",
        "criticality",
        "created_at",
    )

    list_filter = (
        "criticality",
        "organization",
    )

    search_fields = (
        "name",
        "description",
        "impact_description",
    )


@admin.register(
    BusinessProcessDependency
)
class BusinessProcessDependencyAdmin(
    admin.ModelAdmin
):
    list_display = (
        "business_process",
        "asset",
        "dependency_level",
    )

    list_filter = (
        "dependency_level",
        "business_process__organization",
    )

    search_fields = (
        "business_process__name",
        "asset__name",
    )
