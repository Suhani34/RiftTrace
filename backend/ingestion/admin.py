from django.contrib import admin

from .models import IngestionRun


@admin.register(IngestionRun)
class IngestionRunAdmin(
    admin.ModelAdmin
):
    list_display = (
        "id",
        "organization",
        "source_format",
        "created_at",
    )

    list_filter = (
        "source_format",
        "organization",
    )

    readonly_fields = (
        "organization",
        "source_format",
        "source_files",
        "summary",
        "created_at",
    )
