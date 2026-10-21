from django.core.exceptions import ValidationError
from django.db import models


class AttackTechnique(models.Model):
    class Domain(models.TextChoices):
        ENTERPRISE = (
            "ENTERPRISE",
            "Enterprise",
        )


    attack_id = models.CharField(
        max_length=20,
        unique=True,
    )


    name = models.CharField(
        max_length=200,
    )


    domain = models.CharField(
        max_length=20,
        choices=Domain.choices,
        default=Domain.ENTERPRISE,
    )


    tactics = models.JSONField(
        default=list,
    )


    is_subtechnique = models.BooleanField(
        default=False,
    )


    parent_attack_id = models.CharField(
        max_length=20,
        blank=True,
    )


    source_version = models.CharField(
        max_length=20,
        default="20.0",
    )


    source_url = models.URLField()


    enabled = models.BooleanField(
        default=True,
    )


    created_at = models.DateTimeField(
        auto_now_add=True,
    )


    updated_at = models.DateTimeField(
        auto_now=True,
    )


    class Meta:
        ordering = [
            "attack_id",
        ]


    def clean(self):
        if not isinstance(
            self.tactics,
            list,
        ):
            raise ValidationError(
                {
                    "tactics":
                        "Tactics must be stored "
                        "as a JSON list."
                }
            )


    def __str__(self):
        return (
            f"{self.attack_id} — "
            f"{self.name}"
        )


class AttackMappingRule(models.Model):
    class EventType(models.TextChoices):
        VULNERABILITY_EXPLOIT = (
            "VULNERABILITY_EXPLOIT",
            "Vulnerability Exploit",
        )

        CREDENTIAL_DISCOVERY = (
            "CREDENTIAL_DISCOVERY",
            "Credential Discovery",
        )

        IDENTITY_ACCESS = (
            "IDENTITY_ACCESS",
            "Identity Access",
        )

        IDENTITY_LINK = (
            "IDENTITY_LINK",
            "Identity Link",
        )


    rule_code = models.CharField(
        max_length=100,
        unique=True,
    )


    name = models.CharField(
        max_length=200,
    )


    event_type = models.CharField(
        max_length=50,
        choices=EventType.choices,
    )


    technique = models.ForeignKey(
        AttackTechnique,
        on_delete=models.PROTECT,
        related_name="mapping_rules",
    )


    conditions = models.JSONField(
        default=dict,
    )


    rationale = models.TextField()


    priority = models.PositiveIntegerField(
        default=100,
    )


    enabled = models.BooleanField(
        default=True,
    )


    created_at = models.DateTimeField(
        auto_now_add=True,
    )


    updated_at = models.DateTimeField(
        auto_now=True,
    )


    class Meta:
        ordering = [
            "priority",
            "rule_code",
        ]


    def clean(self):
        if not isinstance(
            self.conditions,
            dict,
        ):
            raise ValidationError(
                {
                    "conditions":
                        "Conditions must be "
                        "stored as a JSON object."
                }
            )


    def __str__(self):
        return (
            f"{self.rule_code}: "
            f"{self.technique.attack_id}"
        )
