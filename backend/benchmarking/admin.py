from django.contrib import admin

from .models import BenchmarkResult


@admin.register(BenchmarkResult)
class BenchmarkResultAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "variant",
        "asset_count",
        "mean_ms",
        "p95_ms",
        "mean_query_count",
        "created_at",
    )

    list_filter = (
        "variant",
        "name",
    )

    search_fields = (
        "name",
        "endpoint",
    )
