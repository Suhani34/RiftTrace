from rest_framework import serializers

from .models import Asset, Relationship


class AssetSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(
        source="organization.name",
        read_only=True,
    )

    asset_type_display = serializers.CharField(
        source="get_asset_type_display",
        read_only=True,
    )

    criticality_display = serializers.CharField(
        source="get_criticality_display",
        read_only=True,
    )

    class Meta:
        model = Asset

        fields = (
            "id",
            "organization",
            "organization_name",
            "name",
            "asset_type",
            "asset_type_display",
            "criticality",
            "criticality_display",
            "description",
            "is_internet_exposed",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

    def validate(self, attrs):
        organization = attrs.get(
            "organization",
            getattr(self.instance, "organization", None),
        )

        name = attrs.get(
            "name",
            getattr(self.instance, "name", None),
        )

        if organization is not None and name:
            duplicate_assets = Asset.objects.filter(
                organization=organization,
                name=name,
            )

            if self.instance is not None:
                duplicate_assets = duplicate_assets.exclude(
                    pk=self.instance.pk
                )

            if duplicate_assets.exists():
                raise serializers.ValidationError(
                    {
                        "name": (
                            "An asset with this name already exists "
                            "in this organization."
                        )
                    }
                )

        return attrs

class RelationshipSerializer(serializers.ModelSerializer):
    source_name = serializers.CharField(
        source="source.name",
        read_only=True,
    )

    target_name = serializers.CharField(
        source="target.name",
        read_only=True,
    )

    organization = serializers.IntegerField(
        source="source.organization_id",
        read_only=True,
    )

    relationship_type_display = serializers.CharField(
        source="get_relationship_type_display",
        read_only=True,
    )

    class Meta:
        model = Relationship

        fields = (
            "id",
            "organization",
            "source",
            "source_name",
            "target",
            "target_name",
            "relationship_type",
            "relationship_type_display",
            "description",
            "created_at",
        )

        read_only_fields = (
            "id",
            "organization",
            "created_at",
        )

    def validate(self, attrs):
        source = attrs.get(
            "source",
            getattr(self.instance, "source", None),
        )

        target = attrs.get(
            "target",
            getattr(self.instance, "target", None),
        )

        relationship_type = attrs.get(
            "relationship_type",
            getattr(
                self.instance,
                "relationship_type",
                None,
            ),
        )

        if source is not None and target is not None:
            if source.pk == target.pk:
                raise serializers.ValidationError(
                    {
                        "target": (
                            "An asset cannot have a relationship "
                            "to itself."
                        )
                    }
                )

            if (
                source.organization_id
                != target.organization_id
            ):
                raise serializers.ValidationError(
                    {
                        "target": (
                            "Source and target assets must belong "
                            "to the same organization."
                        )
                    }
                )

        if (
            source is not None
            and target is not None
            and relationship_type is not None
        ):
            duplicate_relationships = Relationship.objects.filter(
                source=source,
                target=target,
                relationship_type=relationship_type,
            )

            if self.instance is not None:
                duplicate_relationships = (
                    duplicate_relationships.exclude(
                        pk=self.instance.pk
                    )
                )

            if duplicate_relationships.exists():
                raise serializers.ValidationError(
                    {
                        "non_field_errors": [
                            (
                                "This relationship already exists."
                            )
                        ]
                    }
                )

        return attrs
