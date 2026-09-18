from django.contrib import admin

from .models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "name",
    )
