from django.core.exceptions import ValidationError
from django.db import models

from organizations.models import Organization


class Asset(models.Model):
    class AssetType(models.TextChoices):
        APPLICATION = "APPLICATION", "Application"
        API = "API", "API"
        SERVER = "SERVER", "Server"
        DATABASE = "DATABASE", "Database"
        WORKSTATION = "WORKSTATION", "Workstation"
        FILE_SERVER = "FILE_SERVER", "File Server"
        VPN_GATEWAY = "VPN_GATEWAY", "VPN Gateway"
        CLOUD_SERVICE = "CLOUD_SERVICE", "Cloud Service"
        CI_CD = "CI_CD", "CI/CD System"
        EMAIL_SERVER = "EMAIL_SERVER", "Email Server"
        DOMAIN_CONTROLLER = "DOMAIN_CONTROLLER", "Domain Controller"
        NETWORK_DEVICE = "NETWORK_DEVICE", "Network Device"
        OTHER = "OTHER", "Other"

    class Criticality(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"
        CRITICAL = "CRITICAL", "Critical"

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="assets",
    )

    name = models.CharField(
        max_length=150,
    )

    asset_type = models.CharField(
        max_length=32,
        choices=AssetType.choices,
        default=AssetType.OTHER,
    )

    criticality = models.CharField(
        max_length=16,
        choices=Criticality.choices,
        default=Criticality.MEDIUM,
    )

    description = models.TextField(
        blank=True,
    )

    is_internet_exposed = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["organization_id", "name"]

        constraints = [
            models.UniqueConstraint(
                fields=["organization", "name"],
                name="unique_asset_name_per_organization",
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_asset_type_display()})"

class Relationship(models.Model):
    class RelationshipType(models.TextChoices):
        CONNECTS_TO = "CONNECTS_TO", "Connects To"
        CALLS = "CALLS", "Calls"
        READS = "READS", "Reads"
        WRITES = "WRITES", "Writes"
        AUTHENTICATES_TO = "AUTHENTICATES_TO", "Authenticates To"
        DEPENDS_ON = "DEPENDS_ON", "Depends On"

    source = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name="outgoing_relationships",
    )

    target = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name="incoming_relationships",
    )

    relationship_type = models.CharField(
        max_length=32,
        choices=RelationshipType.choices,
    )

    description = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = [
            "source_id",
            "target_id",
            "relationship_type",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "source",
                    "target",
                    "relationship_type",
                ],
                name="unique_asset_relationship",
            ),

            models.CheckConstraint(
                condition=~models.Q(
                    source=models.F("target"),
                ),
                name="relationship_source_not_target",
            ),
        ]

    def clean(self):
        super().clean()

        if (
            self.source_id
            and self.target_id
            and self.source.organization_id
            != self.target.organization_id
        ):
            raise ValidationError(
                "Relationships must connect assets "
                "within the same organization."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.source.name} "
            f"--{self.get_relationship_type_display()}--> "
            f"{self.target.name}"
        )
