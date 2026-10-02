from rest_framework import serializers

from .models import (
    BusinessProcess,
    BusinessProcessDependency,
)


class BusinessProcessSerializer(
    serializers.ModelSerializer
):
    organization_name = (
        serializers.CharField(
            source=(
                "organization.name"
            ),
            read_only=True,
        )
    )

    criticality_display = (
        serializers.CharField(
            source=(
                "get_criticality_display"
            ),
            read_only=True,
        )
    )

    class Meta:
        model = BusinessProcess

        fields = [
            "id",
            "organization",
            "organization_name",
            "name",
            "criticality",
            "criticality_display",
            "description",
            "impact_description",
            "created_at",
            "updated_at",
        ]


class BusinessProcessDependencySerializer(
    serializers.ModelSerializer
):
    business_process_name = (
        serializers.CharField(
            source=(
                "business_process.name"
            ),
            read_only=True,
        )
    )

    asset_name = (
        serializers.CharField(
            source="asset.name",
            read_only=True,
        )
    )

    organization = (
        serializers.IntegerField(
            source=(
                "business_process."
                "organization_id"
            ),
            read_only=True,
        )
    )

    dependency_level_display = (
        serializers.CharField(
            source=(
                "get_dependency_level_display"
            ),
            read_only=True,
        )
    )

    class Meta:
        model = (
            BusinessProcessDependency
        )

        fields = [
            "id",
            "organization",
            "business_process",
            "business_process_name",
            "asset",
            "asset_name",
            "dependency_level",
            "dependency_level_display",
            "description",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        business_process = (
            attrs.get(
                "business_process"
            )
            or getattr(
                self.instance,
                "business_process",
                None,
            )
        )

        asset = (
            attrs.get("asset")
            or getattr(
                self.instance,
                "asset",
                None,
            )
        )

        if (
            business_process
            and asset
            and (
                business_process
                .organization_id
                !=
                asset.organization_id
            )
        ):
            raise (
                serializers.ValidationError(
                    {
                        "asset": (
                            "The asset must "
                            "belong to the same "
                            "organization as the "
                            "business process."
                        )
                    }
                )
            )

        return attrs
