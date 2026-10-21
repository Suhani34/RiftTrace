from rest_framework import serializers

from .models import (
    AttackMappingRule,
    AttackTechnique,
)


class AttackTechniqueSerializer(
    serializers.ModelSerializer
):
    domain_display = (
        serializers.CharField(
            source="get_domain_display",

            read_only=True,
        )
    )


    class Meta:
        model = AttackTechnique

        fields = [
            "id",
            "attack_id",
            "name",
            "domain",
            "domain_display",
            "tactics",
            "is_subtechnique",
            "parent_attack_id",
            "source_version",
            "source_url",
            "enabled",
        ]


class AttackMappingRuleSerializer(
    serializers.ModelSerializer
):
    technique_attack_id = (
        serializers.CharField(
            source=(
                "technique.attack_id"
            ),

            read_only=True,
        )
    )


    technique_name = (
        serializers.CharField(
            source=(
                "technique.name"
            ),

            read_only=True,
        )
    )


    class Meta:
        model = AttackMappingRule

        fields = [
            "id",
            "rule_code",
            "name",
            "event_type",
            "technique",
            "technique_attack_id",
            "technique_name",
            "conditions",
            "rationale",
            "priority",
            "enabled",
        ]


class AttackMappingEvaluateSerializer(
    serializers.Serializer
):
    event_type = (
        serializers.ChoiceField(
            choices=(
                AttackMappingRule
                .EventType
                .choices
            )
        )
    )


    attributes = serializers.JSONField(
        required=False,
        default=dict,
    )


    def validate_attributes(
        self,
        value,
    ):
        if not isinstance(
            value,
            dict,
        ):
            raise (
                serializers
                .ValidationError(
                    (
                        "attributes must "
                        "be a JSON object."
                    )
                )
            )


        return value
