from rest_framework import serializers

from assets.models import Asset

from organizations.models import (
    Organization,
)


class ReachabilitySimulationRequestSerializer(
    serializers.Serializer
):
    organization = (
        serializers
        .PrimaryKeyRelatedField(
            queryset=(
                Organization
                .objects
                .all()
            )
        )
    )

    start_asset = (
        serializers
        .PrimaryKeyRelatedField(
            queryset=(
                Asset
                .objects
                .select_related(
                    "organization",
                    "network_zone",
                )
            )
        )
    )


    def validate(self, attrs):
        organization = attrs[
            "organization"
        ]

        start_asset = attrs[
            "start_asset"
        ]


        if (
            start_asset.organization_id
            != organization.id
        ):
            raise serializers.ValidationError(
                {
                    "start_asset": (
                        "The start asset must "
                        "belong to the selected "
                        "organization."
                    )
                }
            )


        return attrs

class AttackPropagationRequestSerializer(
    serializers.Serializer
):
    organization = (
        serializers
        .PrimaryKeyRelatedField(
            queryset=(
                Organization
                .objects
                .all()
            )
        )
    )

    start_asset = (
        serializers
        .PrimaryKeyRelatedField(
            queryset=(
                Asset
                .objects
                .select_related(
                    "organization",
                    "network_zone",
                )
            )
        )
    )

    start_privilege = (
        serializers.ChoiceField(
            choices=(
                "LOW",
                "HIGH",
            ),
            default="LOW",
        )
    )

    def validate(self, attrs):
        organization = attrs[
            "organization"
        ]

        start_asset = attrs[
            "start_asset"
        ]

        if (
            start_asset.organization_id
            != organization.id
        ):
            raise serializers.ValidationError(
                {
                    "start_asset": (
                        "The start asset must "
                        "belong to the selected "
                        "organization."
                    )
                }
            )

        return attrs
