from rest_framework import viewsets

from .models import Asset, Relationship
from .serializers import (
    AssetSerializer,
    RelationshipSerializer,
)


class AssetViewSet(viewsets.ModelViewSet):
    serializer_class = AssetSerializer

    def get_queryset(self):
        queryset = Asset.objects.select_related(
            "organization"
        ).all()

        organization = self.request.query_params.get(
            "organization"
        )

        asset_type = self.request.query_params.get(
            "asset_type"
        )

        criticality = self.request.query_params.get(
            "criticality"
        )

        if organization:
            queryset = queryset.filter(
                organization_id=organization
            )

        if asset_type:
            queryset = queryset.filter(
                asset_type=asset_type
            )

        if criticality:
            queryset = queryset.filter(
                criticality=criticality
            )

        return queryset

class RelationshipViewSet(viewsets.ModelViewSet):
    serializer_class = RelationshipSerializer

    def get_queryset(self):
        queryset = Relationship.objects.select_related(
            "source",
            "source__organization",
            "target",
            "target__organization",
        ).all()

        organization = self.request.query_params.get(
            "organization"
        )

        relationship_type = self.request.query_params.get(
            "relationship_type"
        )

        source = self.request.query_params.get(
            "source"
        )

        target = self.request.query_params.get(
            "target"
        )

        if organization:
            queryset = queryset.filter(
                source__organization_id=organization
            )

        if relationship_type:
            queryset = queryset.filter(
                relationship_type=relationship_type
            )

        if source:
            queryset = queryset.filter(
                source_id=source
            )

        if target:
            queryset = queryset.filter(
                target_id=target
            )

        return queryset
