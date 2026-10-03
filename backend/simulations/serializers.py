from rest_framework import serializers

from assets.models import (
    Asset,
    Relationship,
)

from security.models import (
    Vulnerability,
)

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

class CounterfactualSimulationRequestSerializer(
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
                Asset.objects
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

    disabled_relationship_ids = (
        serializers.ListField(
            child=(
                serializers.IntegerField(
                    min_value=1
                )
            ),

            required=False,

            default=list,
        )
    )

    disabled_vulnerability_ids = (
        serializers.ListField(
            child=(
                serializers.IntegerField(
                    min_value=1
                )
            ),

            required=False,

            default=list,
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


        relationship_ids = set(
            attrs.get(
                "disabled_relationship_ids",
                [],
            )
        )


        vulnerability_ids = set(
            attrs.get(
                "disabled_vulnerability_ids",
                [],
            )
        )


        if (
            not relationship_ids
            and not vulnerability_ids
        ):
            raise serializers.ValidationError(
                {
                    "non_field_errors": [
                        (
                            "Select at least one "
                            "relationship or "
                            "vulnerability to "
                            "change in the "
                            "counterfactual."
                        )
                    ]
                }
            )


        valid_relationship_ids = set(
            Relationship.objects.filter(
                id__in=relationship_ids,

                source__organization=(
                    organization
                ),

                target__organization=(
                    organization
                ),
            ).values_list(
                "id",
                flat=True,
            )
        )


        invalid_relationship_ids = (
            relationship_ids
            - valid_relationship_ids
        )


        if invalid_relationship_ids:
            raise serializers.ValidationError(
                {
                    "disabled_relationship_ids": (
                        "These relationships do "
                        "not belong to the "
                        "selected organization: "
                        + ", ".join(
                            str(
                                relationship_id
                            )

                            for relationship_id
                            in sorted(
                                invalid_relationship_ids
                            )
                        )
                    )
                }
            )


        valid_vulnerability_ids = set(
            Vulnerability.objects.filter(
                id__in=vulnerability_ids,

                asset__organization=(
                    organization
                ),
            ).values_list(
                "id",
                flat=True,
            )
        )


        invalid_vulnerability_ids = (
            vulnerability_ids
            - valid_vulnerability_ids
        )


        if invalid_vulnerability_ids:
            raise serializers.ValidationError(
                {
                    "disabled_vulnerability_ids": (
                        "These vulnerabilities "
                        "do not belong to the "
                        "selected organization: "
                        + ", ".join(
                            str(
                                vulnerability_id
                            )

                            for vulnerability_id
                            in sorted(
                                invalid_vulnerability_ids
                            )
                        )
                    )
                }
            )


        attrs[
            "disabled_relationship_ids"
        ] = sorted(
            relationship_ids
        )


        attrs[
            "disabled_vulnerability_ids"
        ] = sorted(
            vulnerability_ids
        )


        return attrs
