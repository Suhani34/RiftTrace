from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models

from assets.models import Asset


class Vulnerability(models.Model):
    class AttackVector(models.TextChoices):
        NETWORK = "NETWORK", "Network"
        ADJACENT = "ADJACENT", "Adjacent"
        LOCAL = "LOCAL", "Local"
        PHYSICAL = "PHYSICAL", "Physical"

    class PrivilegesRequired(
        models.TextChoices
    ):
        NONE = "NONE", "None"
        LOW = "LOW", "Low"
        HIGH = "HIGH", "High"

    class GrantedPrivilege(
        models.TextChoices
    ):
        LOW = "LOW", "Low"
        HIGH = "HIGH", "High"

    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name="vulnerabilities",
    )

    reference_id = models.CharField(
        max_length=64,
        blank=True,
        help_text=(
            "Optional CVE or internal "
            "vulnerability identifier."
        ),
    )

    title = models.CharField(
        max_length=255,
    )

    cvss_score = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ],
    )

    attack_vector = models.CharField(
        max_length=16,
        choices=AttackVector.choices,
    )

    privileges_required = models.CharField(
        max_length=8,
        choices=PrivilegesRequired.choices,
        default=PrivilegesRequired.NONE,
    )

    grants_privilege = models.CharField(
        max_length=8,
        choices=GrantedPrivilege.choices,
        default=GrantedPrivilege.LOW,
    )

    bypasses_authentication = (
        models.BooleanField(
            default=False,
            help_text=(
                "Whether this modeled "
                "vulnerability can bypass an "
                "authentication requirement "
                "on a relationship."
            ),
        )
    )

    is_exploitable = models.BooleanField(
        default=True,
        help_text=(
            "Whether RiftTrace should treat "
            "this vulnerability as usable "
            "in the current model."
        ),
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
            "asset__name",
            "title",
        ]

    def __str__(self):
        identifier = (
            self.reference_id
            or "Unidentified"
        )

        return (
            f"{identifier} - "
            f"{self.asset.name}"
        )
