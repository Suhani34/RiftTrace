from django.db import models


class IngestionRun(models.Model):
    class SourceFormat(
        models.TextChoices
    ):
        JSON = (
            "JSON",
            "JSON",
        )

        CSV = (
            "CSV",
            "CSV",
        )


    organization = models.ForeignKey(
        "organizations.Organization",

        on_delete=models.CASCADE,

        related_name="ingestion_runs",
    )


    source_format = models.CharField(
        max_length=10,

        choices=SourceFormat.choices,
    )


    source_files = models.JSONField(
        default=list,
    )


    summary = models.JSONField(
        default=dict,
    )


    created_at = models.DateTimeField(
        auto_now_add=True,
    )


    class Meta:
        ordering = [
            "-created_at",
            "-id",
        ]


    def __str__(self):
        return (
            f"{self.organization.name} "
            f"{self.source_format} import "
            f"#{self.id}"
        )
