from rest_framework import serializers

from .models import BenchmarkResult


class BenchmarkResultSerializer(
    serializers.ModelSerializer
):
    organization_name = serializers.CharField(
        source="organization.name",
        read_only=True,
    )


    class Meta:
        model = BenchmarkResult

        fields = (
            "id",
            "name",
            "variant",
            "organization",
            "organization_name",
            "endpoint",
            "method",
            "asset_count",
            "relationship_count",
            "iterations",
            "warmup_iterations",
            "mean_ms",
            "median_ms",
            "p95_ms",
            "min_ms",
            "max_ms",
            "peak_memory_kib",
            "mean_query_count",
            "status_code",
            "payload_sha256",
            "samples",
            "notes",
            "created_at",
        )

        read_only_fields = fields
