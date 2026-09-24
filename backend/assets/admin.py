from django.contrib import admin

from .models import (
    Asset,
    NetworkZone,
    Relationship,
)

@admin.register(NetworkZone)
class NetworkZoneAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "organization",
        "zone_type",
    )

    list_filter = (
        "organization",
        "zone_type",
    )

    search_fields = (
        "name",
        "organization__name",
    )

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "organization",
        "asset_type",
        "criticality",
	"environment",
	"network_zone",
	"hostname",
	"ip_address",
        "is_internet_exposed",
    )

    list_filter = (
        "organization",
        "asset_type",
        "criticality",
        "is_internet_exposed",
    )

    search_fields = (
        "name",
        "organization__name",
    )


@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "source",
        "relationship_type",
        "target",
	"protocol",
	"port",
	"requires_authentication",
    )

    list_filter = (
        "relationship_type",
        "source__organization",
    )

    search_fields = (
        "source__name",
        "target__name",
    )
