from django.core.exceptions import (
    ValidationError,
)

from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models

from assets.models import (
    Asset,
    Relationship,
)


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

    bypasses_mfa = models.BooleanField(
        default=False,

        help_text=(
            "Whether this modeled "
            "vulnerability can bypass "
            "an MFA requirement."
        ),
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

class SecurityControl(models.Model):
    class ControlType(
        models.TextChoices
    ):
        NETWORK_SEGMENTATION = (
            "NETWORK_SEGMENTATION",
            "Network Segmentation",
        )

        VULNERABILITY_REMEDIATION = (
            "VULNERABILITY_REMEDIATION",
            "Vulnerability Remediation",
        )

        MFA = (
            "MFA",
            "Multi-Factor Authentication",
        )

        LEAST_PRIVILEGE = (
            "LEAST_PRIVILEGE",
            "Least Privilege",
        )

        AUTHENTICATION_ENFORCEMENT = (
            "AUTHENTICATION_ENFORCEMENT",
            "Authentication Enforcement",
        )


    organization = models.ForeignKey(
        "organizations.Organization",

        on_delete=models.CASCADE,

        related_name="security_controls",
    )


    name = models.CharField(
        max_length=255,
    )


    control_type = models.CharField(
        max_length=40,

        choices=ControlType.choices,
    )


    target_relationship = (
        models.ForeignKey(
            Relationship,

            on_delete=models.CASCADE,

            related_name=(
                "candidate_security_controls"
            ),

            null=True,

            blank=True,
        )
    )


    target_vulnerability = (
        models.ForeignKey(
            Vulnerability,

            on_delete=models.CASCADE,

            related_name=(
                "candidate_security_controls"
            ),

            null=True,

            blank=True,
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
                    "unique_security_control_"
                    "name_per_organization"
                ),
            )
        ]


    def clean(self):
        super().clean()


        relationship_control_types = {
            self.ControlType
            .NETWORK_SEGMENTATION,

            self.ControlType.MFA,

            self.ControlType
            .LEAST_PRIVILEGE,

            self.ControlType
            .AUTHENTICATION_ENFORCEMENT,
        }


        if (
            self.control_type
            == self.ControlType
            .VULNERABILITY_REMEDIATION
        ):
            if (
                not self
                .target_vulnerability_id
            ):
                raise ValidationError(
                    {
                        "target_vulnerability": (
                            "Vulnerability "
                            "remediation requires "
                            "a target "
                            "vulnerability."
                        )
                    }
                )


            if self.target_relationship_id:
                raise ValidationError(
                    {
                        "target_relationship": (
                            "Vulnerability "
                            "remediation must not "
                            "target a relationship."
                        )
                    }
                )


        elif (
            self.control_type
            in relationship_control_types
        ):
            if (
                not self
                .target_relationship_id
            ):
                raise ValidationError(
                    {
                        "target_relationship": (
                            "This control type "
                            "requires a target "
                            "relationship."
                        )
                    }
                )


            if self.target_vulnerability_id:
                raise ValidationError(
                    {
                        "target_vulnerability": (
                            "This control type "
                            "must not target a "
                            "vulnerability."
                        )
                    }
                )


        if self.target_relationship_id:
            relationship_organization_id = (
                self
                .target_relationship
                .source
                .organization_id
            )


            if (
                relationship_organization_id
                != self.organization_id
            ):
                raise ValidationError(
                    {
                        "target_relationship": (
                            "The target "
                            "relationship must "
                            "belong to the same "
                            "organization."
                        )
                    }
                )


        if self.target_vulnerability_id:
            vulnerability_organization_id = (
                self
                .target_vulnerability
                .asset
                .organization_id
            )


            if (
                vulnerability_organization_id
                != self.organization_id
            ):
                raise ValidationError(
                    {
                        "target_vulnerability": (
                            "The target "
                            "vulnerability must "
                            "belong to the same "
                            "organization."
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
            f"{self.name} "
            f"({self.get_control_type_display()})"
        )
