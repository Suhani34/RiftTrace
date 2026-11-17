from django.conf import settings
from django.db import models

from organizations.models import (
    Organization,
)


class OrganizationMembership(
    models.Model
):
    class Role(
        models.TextChoices
    ):
        ADMIN = (
            "ADMIN",
            "Admin",
        )

        ANALYST = (
            "ANALYST",
            "Analyst",
        )

        VIEWER = (
            "VIEWER",
            "Viewer",
        )


    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name=(
            "organization_memberships"
        ),
    )


    organization = (
        models.ForeignKey(
            Organization,

            on_delete=models.CASCADE,

            related_name=(
                "memberships"
            ),
        )
    )


    role = models.CharField(
        max_length=16,

        choices=Role.choices,

        default=Role.VIEWER,
    )


    created_at = (
        models.DateTimeField(
            auto_now_add=True
        )
    )


    updated_at = (
        models.DateTimeField(
            auto_now=True
        )
    )


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "user",
                    "organization",
                ],

                name=(
                    "unique_user_"
                    "organization_membership"
                ),
            )
        ]


    def __str__(self):
        return (
            f"{self.user} - "
            f"{self.organization} "
            f"({self.role})"
        )
