from rest_framework import serializers

from .models import Vulnerability


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
            "is_exploitable",
            "description",
            "created_at",
            "updated_at",
        ]
