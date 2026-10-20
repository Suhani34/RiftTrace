from django.core.exceptions import ValidationError
from django.db import models


class Identity(models.Model):
    class IdentityType(models.TextChoices):
        USER = (
            "USER",
            "User",
        )

        SERVICE_ACCOUNT = (
            "SERVICE_ACCOUNT",
            "Service Account",
        )

        MACHINE_ACCOUNT = (
            "MACHINE_ACCOUNT",
            "Machine Account",
        )

        GROUP = (
            "GROUP",
            "Group",
        )

        ROLE = (
            "ROLE",
            "Role",
        )


    class PrivilegeLevel(models.TextChoices):
        LOW = (
            "LOW",
            "Low",
        )

        HIGH = (
            "HIGH",
            "High",
        )


    organization = models.ForeignKey(
        "organizations.Organization",

        on_delete=models.CASCADE,

        related_name="identities",
    )


    name = models.CharField(
        max_length=200,
    )


    identity_type = models.CharField(
        max_length=30,

        choices=IdentityType.choices,
    )


    privilege_level = models.CharField(
        max_length=10,

        choices=PrivilegeLevel.choices,

        default=PrivilegeLevel.LOW,
    )


    enabled = models.BooleanField(
        default=True,
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
            "name",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "name",
                ],

                name=(
                    "unique_identity_name_per_organization"
                ),
            )
        ]


    def __str__(self):
        return (
            f"{self.name} "
            f"({self.get_identity_type_display()})"
        )


class CredentialExposure(models.Model):
    class CredentialType(models.TextChoices):
        PASSWORD = (
            "PASSWORD",
            "Password",
        )

        API_KEY = (
            "API_KEY",
            "API Key",
        )

        TOKEN = (
            "TOKEN",
            "Token",
        )

        SSH_KEY = (
            "SSH_KEY",
            "SSH Key",
        )

        CERTIFICATE = (
            "CERTIFICATE",
            "Certificate",
        )

        SESSION = (
            "SESSION",
            "Session",
        )


    organization = models.ForeignKey(
        "organizations.Organization",

        on_delete=models.CASCADE,

        related_name="credential_exposures",
    )


    name = models.CharField(
        max_length=200,
    )


    identity = models.ForeignKey(
        Identity,

        on_delete=models.CASCADE,

        related_name="credential_exposures",
    )


    stored_on_asset = models.ForeignKey(
        "assets.Asset",

        on_delete=models.CASCADE,

        related_name="credential_exposures",
    )


    credential_type = models.CharField(
        max_length=20,

        choices=CredentialType.choices,
    )


    discoverable_on_compromise = (
        models.BooleanField(
            default=True,
        )
    )


    satisfies_mfa = models.BooleanField(
        default=False,
    )


    active = models.BooleanField(
        default=True,
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
            "name",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "name",
                ],

                name=(
                    "unique_credential_exposure_name_per_org"
                ),
            )
        ]


    def clean(self):
        if (
            self.identity_id
            and self.organization_id
            and (
                self.identity.organization_id
                != self.organization_id
            )
        ):
            raise ValidationError(
                (
                    "Identity must belong "
                    "to the same organization."
                )
            )


        if (
            self.stored_on_asset_id
            and self.organization_id
            and (
                self.stored_on_asset.organization_id
                != self.organization_id
            )
        ):
            raise ValidationError(
                (
                    "Stored-on asset must "
                    "belong to the same organization."
                )
            )


    def __str__(self):
        return self.name


class IdentityAccess(models.Model):
    class AccessType(models.TextChoices):
        LOGIN = (
            "LOGIN",
            "Login",
        )

        ADMINISTER = (
            "ADMINISTER",
            "Administer",
        )

        API_ACCESS = (
            "API_ACCESS",
            "API Access",
        )

        DATABASE_ACCESS = (
            "DATABASE_ACCESS",
            "Database Access",
        )

        REMOTE_SERVICE = (
            "REMOTE_SERVICE",
            "Remote Service",
        )

        SERVICE_RUN = (
            "SERVICE_RUN",
            "Service Run",
        )


    organization = models.ForeignKey(
        "organizations.Organization",

        on_delete=models.CASCADE,

        related_name="identity_access_rules",
    )


    identity = models.ForeignKey(
        Identity,

        on_delete=models.CASCADE,

        related_name="asset_access_rules",
    )


    asset = models.ForeignKey(
        "assets.Asset",

        on_delete=models.CASCADE,

        related_name="identity_access_rules",
    )


    access_type = models.CharField(
        max_length=30,

        choices=AccessType.choices,
    )


    granted_privilege = models.CharField(
        max_length=10,

        choices=Identity.PrivilegeLevel.choices,

        default=Identity.PrivilegeLevel.LOW,
    )


    requires_mfa = models.BooleanField(
        default=False,
    )


    enabled = models.BooleanField(
        default=True,
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
            "identity__name",
            "asset__name",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "identity",
                    "asset",
                    "access_type",
                ],

                name=(
                    "unique_identity_asset_access"
                ),
            )
        ]


    def clean(self):
        if (
            self.identity_id
            and self.organization_id
            and (
                self.identity.organization_id
                != self.organization_id
            )
        ):
            raise ValidationError(
                (
                    "Identity must belong "
                    "to the same organization."
                )
            )


        if (
            self.asset_id
            and self.organization_id
            and (
                self.asset.organization_id
                != self.organization_id
            )
        ):
            raise ValidationError(
                (
                    "Asset must belong "
                    "to the same organization."
                )
            )


    def __str__(self):
        return (
            f"{self.identity.name} "
            f"→ {self.asset.name}"
        )


class IdentityLink(models.Model):
    class LinkType(models.TextChoices):
        MEMBER_OF = (
            "MEMBER_OF",
            "Member Of",
        )

        ASSUMES_ROLE = (
            "ASSUMES_ROLE",
            "Assumes Role",
        )

        CAN_IMPERSONATE = (
            "CAN_IMPERSONATE",
            "Can Impersonate",
        )

        DELEGATES_TO = (
            "DELEGATES_TO",
            "Delegates To",
        )


    organization = models.ForeignKey(
        "organizations.Organization",

        on_delete=models.CASCADE,

        related_name="identity_links",
    )


    source_identity = models.ForeignKey(
        Identity,

        on_delete=models.CASCADE,

        related_name="outgoing_identity_links",
    )


    target_identity = models.ForeignKey(
        Identity,

        on_delete=models.CASCADE,

        related_name="incoming_identity_links",
    )


    link_type = models.CharField(
        max_length=30,

        choices=LinkType.choices,
    )


    requires_mfa = models.BooleanField(
        default=False,
    )


    enabled = models.BooleanField(
        default=True,
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
            "source_identity__name",
            "target_identity__name",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "source_identity",
                    "target_identity",
                    "link_type",
                ],

                name=(
                    "unique_identity_link"
                ),
            )
        ]


    def clean(self):
        if (
            self.source_identity_id
            == self.target_identity_id
        ):
            raise ValidationError(
                (
                    "An identity cannot link "
                    "to itself."
                )
            )


        if (
            self.source_identity_id
            and self.organization_id
            and (
                self.source_identity.organization_id
                != self.organization_id
            )
        ):
            raise ValidationError(
                (
                    "Source identity must "
                    "belong to the same organization."
                )
            )


        if (
            self.target_identity_id
            and self.organization_id
            and (
                self.target_identity.organization_id
                != self.organization_id
            )
        ):
            raise ValidationError(
                (
                    "Target identity must "
                    "belong to the same organization."
                )
            )


    def __str__(self):
        return (
            f"{self.source_identity.name} "
            f"→ {self.target_identity.name}"
        )
