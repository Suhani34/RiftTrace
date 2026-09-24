from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from assets.models import (
    Asset,
    NetworkZone,
    Relationship,
)

from assets.serializers import (
    AssetSerializer,
    NetworkZoneSerializer,
    RelationshipSerializer,
)

from .models import Organization
from .serializers import OrganizationSerializer


class OrganizationViewSet(
    viewsets.ModelViewSet
):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    @action(
        detail=True,
        methods=["get"],
    )
    def topology(self, request, pk=None):
        organization = self.get_object()

        zones = NetworkZone.objects.filter(
            organization=organization
        )

        assets = (
            Asset.objects
            .filter(
                organization=organization
            )
            .select_related(
                "organization",
                "network_zone",
            )
        )

        relationships = (
            Relationship.objects
            .filter(
                source__organization=organization
            )
            .select_related(
                "source",
                "target",
            )
        )

        return Response(
            {
                "organization":
                    OrganizationSerializer(
                        organization
                    ).data,

                "zones":
                    NetworkZoneSerializer(
                        zones,
                        many=True,
                    ).data,

                "nodes":
                    AssetSerializer(
                        assets,
                        many=True,
                    ).data,

                "edges":
                    RelationshipSerializer(
                        relationships,
                        many=True,
                    ).data,
            }
        )
