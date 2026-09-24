from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Organization
from assets.models import (
    Asset,
    NetworkZone,
    Relationship,
)

class OrganizationModelTests(APITestCase):
    def test_organization_string_representation(self):
        organization = Organization.objects.create(
            name="DemoCorp"
        )

        self.assertEqual(
            str(organization),
            "DemoCorp",
        )


class OrganizationAPITests(APITestCase):
    def test_list_organizations(self):
        Organization.objects.create(
            name="DemoCorp"
        )

        response = self.client.get(
            reverse("organization-list")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

    def test_create_organization(self):
        payload = {
            "name": "CyberLab",
            "description": "API test organization",
        }

        response = self.client.post(
            reverse("organization-list"),
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            Organization.objects.filter(
                name="CyberLab"
            ).exists()
        )

    def test_retrieve_organization(self):
        organization = Organization.objects.create(
            name="DemoCorp"
        )

        response = self.client.get(
            reverse(
                "organization-detail",
                args=[organization.pk],
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["name"],
            "DemoCorp",
        )

class OrganizationTopologyAPITests(
    APITestCase
):
    def test_topology_returns_nodes_and_edges(
        self,
    ):
        organization = (
            Organization.objects.create(
                name="TopologyCorp"
            )
        )

        zone = NetworkZone.objects.create(
            organization=organization,
            name="Internal",
            zone_type=(
                NetworkZone.ZoneType.INTERNAL
            ),
        )

        source = Asset.objects.create(
            organization=organization,
            name="Application",
            asset_type=(
                Asset.AssetType.APPLICATION
            ),
            network_zone=zone,
        )

        target = Asset.objects.create(
            organization=organization,
            name="Database",
            asset_type=(
                Asset.AssetType.DATABASE
            ),
            network_zone=zone,
        )

        Relationship.objects.create(
            source=source,
            target=target,
            relationship_type=(
                Relationship
                .RelationshipType
                .READS
            ),
            protocol="TCP",
            port=5432,
            requires_authentication=True,
        )

        response = self.client.get(
            reverse(
                "organization-topology",
                args=[organization.pk],
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data["zones"]),
            1,
        )

        self.assertEqual(
            len(response.data["nodes"]),
            2,
        )

        self.assertEqual(
            len(response.data["edges"]),
            1,
        )
