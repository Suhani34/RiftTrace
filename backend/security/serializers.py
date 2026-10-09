from rest_framework import serializers

from .models import (
    SecurityControl,
    Vulnerability,
)


class VulnerabilitySerializer(
    serializers.ModelSerializer
):
    asset_name = (
        serializers.CharField(
            source="asset.name",
            read_only=True,
        )
    )

    organization = (
        serializers.IntegerField(
            source=(
                "asset.organization_id"
            ),
            read_only=True,
        )
    )

    attack_vector_display = (
        serializers.CharField(
            source=(
                "get_attack_vector_display"
            ),
            read_only=True,
        )
    )

    privileges_required_display = (
        serializers.CharField(
            source=(
                "get_privileges_required_display"
            ),
            read_only=True,
        )
    )

    grants_privilege_display = (
        serializers.CharField(
            source=(
                "get_grants_privilege_display"
            ),
            read_only=True,
        )
    )

    class Meta:
        model = Vulnerability

        fields = [
            "id",
            "organization",
            "asset",
            "asset_name",
            "reference_id",
            "title",
            "cvss_score",
            "attack_vector",
            "attack_vector_display",
            "privileges_required",
            "privileges_required_display",
            "grants_privilege",
            "grants_privilege_display",
            "bypasses_authentication",
	    "bypasses_mfa",
            "is_exploitable",
            "description",
            "created_at",
            "updated_at",
        ]

class SecurityControlSerializer(
    serializers.ModelSerializer
):
    organization_name = (
        serializers.CharField(
            source="organization.name",

            read_only=True,
        )
    )


    control_type_display = (
        serializers.CharField(
            source=(
                "get_control_type_display"
            ),

            read_only=True,
        )
    )


    target_relationship_display = (
        serializers
        .SerializerMethodField()
    )


    target_vulnerability_display = (
        serializers
        .SerializerMethodField()
    )


    class Meta:
        model = SecurityControl

        fields = [
            "id",

            "organization",
            "organization_name",

            "name",

            "control_type",
            "control_type_display",

            "target_relationship",
            "target_relationship_display",

            "target_vulnerability",
            "target_vulnerability_display",

            "description",

            "created_at",
            "updated_at",
        ]


    def get_target_relationship_display(
        self,
        obj,
    ):
        relationship = (
            obj.target_relationship
        )


        if relationship is None:
            return None


        return (
            f"{relationship.source.name}"
            " → "
            f"{relationship.target.name}"
            " ("
            f"{relationship.get_relationship_type_display()}"
            ")"
        )


    def get_target_vulnerability_display(
        self,
        obj,
    ):
        vulnerability = (
            obj.target_vulnerability
        )


        if vulnerability is None:
            return None


        identifier = (
            vulnerability.reference_id
            or vulnerability.title
        )


        return (
            f"{identifier}"
            " — "
            f"{vulnerability.asset.name}"
        )


    def validate(self, attrs):
        instance = self.instance


        organization = (
            attrs["organization"]

            if "organization" in attrs

            else getattr(
                instance,
                "organization",
                None,
            )
        )


        control_type = (
            attrs["control_type"]

            if "control_type" in attrs

            else getattr(
                instance,
                "control_type",
                None,
            )
        )


        target_relationship = (
            attrs["target_relationship"]

            if "target_relationship"
            in attrs

            else getattr(
                instance,
                "target_relationship",
                None,
            )
        )


        target_vulnerability = (
            attrs["target_vulnerability"]

            if "target_vulnerability"
            in attrs

            else getattr(
                instance,
                "target_vulnerability",
                None,
            )
        )


        relationship_types = {
            SecurityControl
            .ControlType
            .NETWORK_SEGMENTATION,

            SecurityControl
            .ControlType
            .MFA,

            SecurityControl
            .ControlType
            .LEAST_PRIVILEGE,

            SecurityControl
            .ControlType
            .AUTHENTICATION_ENFORCEMENT,
        }


        if (
            control_type
            == SecurityControl
            .ControlType
            .VULNERABILITY_REMEDIATION
        ):
            if target_vulnerability is None:
                raise serializers.ValidationError(
                    {
                        "target_vulnerability": (
                            "Select a target "
                            "vulnerability."
                        )
                    }
                )


            if target_relationship is not None:
                raise serializers.ValidationError(
                    {
                        "target_relationship": (
                            "Vulnerability "
                            "remediation cannot "
                            "target a relationship."
                        )
                    }
                )


        elif control_type in relationship_types:
            if target_relationship is None:
                raise serializers.ValidationError(
                    {
                        "target_relationship": (
                            "Select a target "
                            "relationship."
                        )
                    }
                )


            if target_vulnerability is not None:
                raise serializers.ValidationError(
                    {
                        "target_vulnerability": (
                            "This control cannot "
                            "target a "
                            "vulnerability."
                        )
                    }
                )


        if (
            target_relationship
            and organization
            and (
                target_relationship
                .source
                .organization_id
                != organization.id
            )
        ):
            raise serializers.ValidationError(
                {
                    "target_relationship": (
                        "The relationship must "
                        "belong to the selected "
                        "organization."
                    )
                }
            )


        if (
            target_vulnerability
            and organization
            and (
                target_vulnerability
                .asset
                .organization_id
                != organization.id
            )
        ):
            raise serializers.ValidationError(
                {
                    "target_vulnerability": (
                        "The vulnerability must "
                        "belong to the selected "
                        "organization."
                    )
                }
            )


        return attrs
