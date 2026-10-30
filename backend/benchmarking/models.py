from django.db import models

from organizations.models import Organization


class BenchmarkResult(models.Model):
    class Variant(models.TextChoices):
        BASELINE = (
            "BASELINE",
            "Baseline",
        )

        OPTIMIZED = (
            "OPTIMIZED",
            "Optimized",
        )


    name = models.CharField(
        max_length=200,
    )

    variant = models.CharField(
        max_length=20,
        choices=Variant.choices,
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="benchmark_results",
    )

    endpoint = models.CharField(
        max_length=300,
    )

    method = models.CharField(
        max_length=10,
        default="POST",
    )

    asset_count = models.PositiveIntegerField(
        default=0,
    )

    relationship_count = models.PositiveIntegerField(
        default=0,
    )

    iterations = models.PositiveIntegerField()

    warmup_iterations = models.PositiveIntegerField()

    mean_ms = models.FloatField()

    median_ms = models.FloatField()

    p95_ms = models.FloatField()

    min_ms = models.FloatField()

    max_ms = models.FloatField()

    peak_memory_kib = models.FloatField()

    mean_query_count = models.FloatField()

    status_code = models.PositiveIntegerField()

    payload_sha256 = models.CharField(
        max_length=64,
        blank=True,
    )

    samples = models.JSONField(
        default=list,
    )

    notes = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )


    class Meta:
        ordering = (
            "-created_at",
            "-id",
        )

        indexes = [
            models.Index(
                fields=(
                    "name",
                    "variant",
                    "asset_count",
                ),

                name="benchmark_lookup_idx",
            ),
        ]


    def __str__(self):
        return (
            f"{self.name}"
            f" - {self.variant}"
            f" - {self.asset_count} assets"
        )
