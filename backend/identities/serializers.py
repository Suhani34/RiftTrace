from rest_framework import serializers

from .models import (
    CredentialExposure,
    Identity,
    IdentityAccess,
    IdentityLink,
)


class IdentitySerializer(
    serializers.ModelSerializer
):
    identity_type_display = (
        serializers.CharField(
            source="get_identity_type_display",

            read_only=True,
        )
    )


    privilege_level_display = (
        serializers.CharField(
            source="get_privilege_level_display",

            read_only=True,
        )
    )


    class Meta:
        model = Identity

        fields = [
            "id",
            "organization",
            "name",
            "identity_type",
            "identity_type_display",
            "privilege_level",
            "privilege_level_display",
            "enabled",
            "description",
            "created_at",
            "updated_at",
        ]


class CredentialExposureSerializer(
    serializers.ModelSerializer
):
    identity_name = serializers.CharField(
        source="identity.name",

        read_only=True,
    )


    stored_on_asset_name = (
        serializers.CharField(
            source="stored_on_asset.name",

            read_only=True,
        )
    )


    class Meta:
        model = CredentialExposure

        fields = [
            "id",
            "organization",
            "name",
            "identity",
            "identity_name",
            "stored_on_asset",
            "stored_on_asset_name",
            "credential_type",
            "discoverable_on_compromise",
            "satisfies_mfa",
            "active",
            "description",
            "created_at",
            "updated_at",
        ]


    def validate(self, attrs):
        organization = attrs.get(
            "organization",

            getattr(
                self.instance,
                "organization",
                None,
            ),
        )


        identity = attrs.get(
            "identity",

            getattr(
                self.instance,
                "identity",
                None,
            ),
        )


        asset = attrs.get(
            "stored_on_asset",

            getattr(
                self.instance,
                "stored_on_asset",
                None,
            ),
        )


        if (
            organization
            and identity
            and (
                identity.organization_id
                != organization.id
            )
        ):
            raise serializers.ValidationError(
                (
                    "Identity must belong "
                    "to the selected organization."
                )
            )


        if (
            organization
            and asset
            and (
                asset.organization_id
                != organization.id
            )
        ):
            raise serializers.ValidationError(
                (
                    "Asset must belong "
                    "to the selected organization."
                )
            )


        return attrs


class IdentityAccessSerializer(
    serializers.ModelSerializer
):
    identity_name = serializers.CharField(
        source="identity.name",

        read_only=True,
    )


    asset_name = serializers.CharField(
        source="asset.name",

        read_only=True,
    )


    class Meta:
        model = IdentityAccess

        fields = [
            "id",
            "organization",
            "identity",
            "identity_name",
            "asset",
            "asset_name",
            "access_type",
            "granted_privilege",
            "requires_mfa",
            "enabled",
            "description",
            "created_at",
            "updated_at",
        ]


    def validate(self, attrs):
        organization = attrs.get(
            "organization",

            getattr(
                self.instance,
                "organization",
                None,
            ),
        )


        identity = attrs.get(
            "identity",

            getattr(
                self.instance,
                "identity",
                None,
            ),
        )


        asset = attrs.get(
            "asset",

            getattr(
                self.instance,
                "asset",
                None,
            ),
        )


        if (
            organization
            and identity
            and (
                identity.organization_id
                != organization.id
            )
        ):
            raise serializers.ValidationError(
                (
                    "Identity belongs to "
                    "another organization."
                )
            )


        if (
            organization
            and asset
            and (
                asset.organization_id
                != organization.id
            )
        ):
            raise serializers.ValidationError(
                (
                    "Asset belongs to "
                    "another organization."
                )
            )


        return attrs


class IdentityLinkSerializer(
    serializers.ModelSerializer
):
    source_identity_name = (
        serializers.CharField(
            source="source_identity.name",

            read_only=True,
        )
    )


    target_identity_name = (
        serializers.CharField(
            source="target_identity.name",

            read_only=True,
        )
    )


    class Meta:
        model = IdentityLink

        fields = [
            "id",
            "organization",
            "source_identity",
            "source_identity_name",
            "target_identity",
            "target_identity_name",
            "link_type",
            "requires_mfa",
            "enabled",
            "description",
            "created_at",
            "updated_at",
        ]


    def validate(self, attrs):
        organization = attrs.get(
            "organization",

            getattr(
                self.instance,
                "organization",
                None,
            ),
        )


        source = attrs.get(
            "source_identity",

            getattr(
                self.instance,
                "source_identity",
                None,
            ),
        )


        target = attrs.get(
            "target_identity",

            getattr(
                self.instance,
                "target_identity",
                None,
            ),
        )


        if (
            source
            and target
            and source.id == target.id
        ):
            raise serializers.ValidationError(
                (
                    "Source and target identity "
                    "cannot be the same."
                )
            )


        for identity in (
            source,
            target,
        ):
            if (
                organization
                and identity
                and (
                    identity.organization_id
                    != organization.id
                )
            ):
                raise serializers.ValidationError(
                    (
                        "Both identities must "
                        "belong to the selected "
                        "organization."
                    )
                )


        return attrs
