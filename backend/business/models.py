from django.core.exceptions import (
    ValidationError,
)
from django.db import models

from assets.models import Asset
from organizations.models import (
    Organization,
)


class BusinessProcess(models.Model):
    class Criticality(
        models.TextChoices
    ):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"
        CRITICAL = (
            "CRITICAL",
            "Critical",
        )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name=(
            "business_processes"
        ),
    )

    name = models.CharField(
        max_length=255,
    )

    criticality = models.CharField(
        max_length=16,
        choices=Criticality.choices,
        default=Criticality.MEDIUM,
    )

    description = models.TextField(
        blank=True,
    )

    impact_description = models.TextField(
        blank=True,
        help_text=(
            "Human-readable description "
            "of the potential business "
            "consequence if this process "
            "is affected."
        ),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = [
            "organization__name",
            "name",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "name",
                ],
                name=(
                    "unique_business_process_"
                    "name_per_organization"
                ),
            )
        ]

    def __str__(self):
        return (
            f"{self.organization.name} - "
            f"{self.name}"
        )


class BusinessProcessDependency(
    models.Model
):
    class DependencyLevel(
        models.TextChoices
    ):
        SUPPORTING = (
            "SUPPORTING",
            "Supporting",
        )

        IMPORTANT = (
            "IMPORTANT",
            "Important",
        )

        ESSENTIAL = (
            "ESSENTIAL",
            "Essential",
        )

    business_process = (
        models.ForeignKey(
            BusinessProcess,
            on_delete=models.CASCADE,
            related_name=(
                "asset_dependencies"
            ),
        )
    )

    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name=(
            "business_process_dependencies"
        ),
    )

    dependency_level = (
        models.CharField(
            max_length=16,
            choices=(
                DependencyLevel.choices
            ),
            default=(
                DependencyLevel.IMPORTANT
            ),
        )
    )

    description = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = [
            "business_process__name",
            "asset__name",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "business_process",
                    "asset",
                ],
                name=(
                    "unique_asset_dependency_"
                    "per_business_process"
                ),
            )
        ]

    def clean(self):
        super().clean()

        if (
            self.business_process_id
            and self.asset_id
            and (
                self.business_process
                .organization_id
                !=
                self.asset.organization_id
            )
        ):
            raise ValidationError(
                {
                    "asset": (
                        "The asset must belong "
                        "to the same organization "
                        "as the business process."
                    )
                }
            )

    def save(
        self,
        *args,
        **kwargs,
    ):
        self.full_clean()

        return super().save(
            *args,
            **kwargs,
        )

    def __str__(self):
        return (
            f"{self.business_process.name}"
            f" -> {self.asset.name}"
        )
