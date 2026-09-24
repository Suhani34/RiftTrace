from rest_framework import serializers

from .models import (
  Asset,
  NetworkZone,
  Relationship,
)

class NetworkZoneSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(
        source="organization.name",
        read_only=True,
    )

    zone_type_display = serializers.CharField(
        source="get_zone_type_display",
        read_only=True,
    )

    class Meta:
        model = NetworkZone

        fields = (
            "id",
            "organization",
            "organization_name",
            "name",
            "zone_type",
            "zone_type_display",
            "description",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

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

    network_zone_name = serializers.CharField(
        source="network_zone.name",
        read_only=True,
        allow_null=True,
    )

    environment_display = serializers.CharField(
        source="get_environment_display",
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
	    "environment",
	    "environment_display",
	    "network_zone",
	    "network_zone_name",
	    "hostname",
	    "ip_address",
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

        network_zone = attrs.get(
            "network_zone",
            getattr(
                self.instance,
                "network_zone",
                None,
            ),
        )

        if (
            organization is not None
            and network_zone is not None
            and network_zone.organization_id
            != organization.id
        ):
            raise serializers.ValidationError(
                {
                    "network_zone": (
                        "The network zone must belong "
                        "to the selected organization."
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
	    "protocol",
	    "port",
	    "requires_authentication",
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
