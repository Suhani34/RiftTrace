from rest_framework import viewsets

from .models import Vulnerability
from .serializers import (
    VulnerabilitySerializer,
)


class VulnerabilityViewSet(
    viewsets.ModelViewSet
):
    serializer_class = (
        VulnerabilitySerializer
    )

    queryset = (
        Vulnerability.objects
        .select_related(
            "asset",
            "asset__organization",
            "asset__network_zone",
        )
        .all()
    )

    def get_queryset(self):
        queryset = super().get_queryset()

        organization = (
            self.request
            .query_params
            .get("organization")
        )

        asset = (
            self.request
            .query_params
            .get("asset")
        )

        attack_vector = (
            self.request
            .query_params
            .get("attack_vector")
        )

        is_exploitable = (
            self.request
            .query_params
            .get("is_exploitable")
        )

        if organization:
            queryset = queryset.filter(
                asset__organization_id=(
                    organization
                )
            )

        if asset:
            queryset = queryset.filter(
                asset_id=asset
            )

        if attack_vector:
            queryset = queryset.filter(
                attack_vector=(
                    attack_vector
                )
            )

        if is_exploitable in {
            "true",
            "false",
        }:
            queryset = queryset.filter(
                is_exploitable=(
                    is_exploitable
                    == "true"
                )
            )

        return queryset

