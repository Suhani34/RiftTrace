from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from organizations.models import Organization

from .models import Asset, Relationship


class AssetAndRelationshipModelTests(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(
            name="DemoCorp"
        )

        self.web = Asset.objects.create(
            organization=self.organization,
            name="Public Web App",
            asset_type=Asset.AssetType.APPLICATION,
            criticality=Asset.Criticality.HIGH,
            is_internet_exposed=True,
        )

        self.api = Asset.objects.create(
            organization=self.organization,
            name="Internal API",
            asset_type=Asset.AssetType.API,
            criticality=Asset.Criticality.HIGH,
        )

    def test_asset_belongs_to_organization(self):
        self.assertEqual(
            self.web.organization,
            self.organization,
        )

    def test_asset_name_must_be_unique_within_organization(self):
        duplicate = Asset(
            organization=self.organization,
            name="Public Web App",
            asset_type=Asset.AssetType.APPLICATION,
        )

        with self.assertRaises(ValidationError):
            duplicate.full_clean()

    def test_relationship_creates_directed_connection(self):
        relationship = Relationship.objects.create(
            source=self.web,
            target=self.api,
            relationship_type=(
                Relationship.RelationshipType.CALLS
            ),
        )

        self.assertEqual(
            relationship.source,
            self.web,
        )

        self.assertEqual(
            relationship.target,
            self.api,
        )

        self.assertIn(
            relationship,
            self.web.outgoing_relationships.all(),
        )

    def test_relationship_cannot_connect_different_organizations(self):
        another_organization = Organization.objects.create(
            name="AnotherCorp"
        )

        other_asset = Asset.objects.create(
            organization=another_organization,
            name="Other Server",
            asset_type=Asset.AssetType.SERVER,
        )

        with self.assertRaises(ValidationError):
            Relationship.objects.create(
                source=self.web,
                target=other_asset,
                relationship_type=(
                    Relationship.RelationshipType.CONNECTS_TO
                ),
            )

    def test_relationship_cannot_point_to_same_asset(self):
        with self.assertRaises(ValidationError):
            Relationship.objects.create(
                source=self.web,
                target=self.web,
                relationship_type=(
                    Relationship.RelationshipType.CONNECTS_TO
                ),
            )

class AssetAPITests(APITestCase):
    def setUp(self):
        self.organization = Organization.objects.create(
            name="DemoCorp"
        )

    def test_create_asset(self):
        payload = {
            "organization": self.organization.pk,
            "name": "Public Web Server",
            "asset_type": Asset.AssetType.SERVER,
            "criticality": Asset.Criticality.HIGH,
            "is_internet_exposed": True,
        }

        response = self.client.post(
            reverse("asset-list"),
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            Asset.objects.filter(
                organization=self.organization,
                name="Public Web Server",
            ).exists()
        )

    def test_list_assets(self):
        Asset.objects.create(
            organization=self.organization,
            name="Database",
            asset_type=Asset.AssetType.DATABASE,
        )

        response = self.client.get(
            reverse("asset-list")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

    def test_filter_assets_by_criticality(self):
        Asset.objects.create(
            organization=self.organization,
            name="Critical Database",
            asset_type=Asset.AssetType.DATABASE,
            criticality=Asset.Criticality.CRITICAL,
        )

        Asset.objects.create(
            organization=self.organization,
            name="Low Value Server",
            asset_type=Asset.AssetType.SERVER,
            criticality=Asset.Criticality.LOW,
        )

        response = self.client.get(
            reverse("asset-list"),
            {
                "criticality": Asset.Criticality.CRITICAL
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["name"],
            "Critical Database",
        )

    def test_patch_asset(self):
        asset = Asset.objects.create(
            organization=self.organization,
            name="Application Server",
            asset_type=Asset.AssetType.SERVER,
            criticality=Asset.Criticality.MEDIUM,
        )

        response = self.client.patch(
            reverse(
                "asset-detail",
                args=[asset.pk],
            ),
            {
                "criticality": (
                    Asset.Criticality.CRITICAL
                )
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        asset.refresh_from_db()

        self.assertEqual(
            asset.criticality,
            Asset.Criticality.CRITICAL,
        )

    def test_duplicate_asset_name_is_rejected(self):
        Asset.objects.create(
            organization=self.organization,
            name="Public Web Server",
            asset_type=Asset.AssetType.SERVER,
        )

        response = self.client.post(
            reverse("asset-list"),
            {
                "organization": self.organization.pk,
                "name": "Public Web Server",
                "asset_type": Asset.AssetType.SERVER,
                "criticality": Asset.Criticality.MEDIUM,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

class RelationshipAPITests(APITestCase):
    def setUp(self):
        self.organization = Organization.objects.create(
            name="DemoCorp"
        )

        self.web = Asset.objects.create(
            organization=self.organization,
            name="Web Server",
            asset_type=Asset.AssetType.SERVER,
        )

        self.api = Asset.objects.create(
            organization=self.organization,
            name="Internal API",
            asset_type=Asset.AssetType.API,
        )

    def test_create_relationship(self):
        payload = {
            "source": self.web.pk,
            "target": self.api.pk,
            "relationship_type": (
                Relationship.RelationshipType.CONNECTS_TO
            ),
        }

        response = self.client.post(
            reverse("relationship-list"),
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            Relationship.objects.filter(
                source=self.web,
                target=self.api,
            ).exists()
        )

    def test_self_relationship_is_rejected(self):
        response = self.client.post(
            reverse("relationship-list"),
            {
                "source": self.web.pk,
                "target": self.web.pk,
                "relationship_type": (
                    Relationship.RelationshipType.CONNECTS_TO
                ),
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_cross_organization_relationship_is_rejected(self):
        second_organization = (
            Organization.objects.create(
                name="AnotherCorp"
            )
        )

        other_server = Asset.objects.create(
            organization=second_organization,
            name="Other Server",
            asset_type=Asset.AssetType.SERVER,
        )

        response = self.client.post(
            reverse("relationship-list"),
            {
                "source": self.web.pk,
                "target": other_server.pk,
                "relationship_type": (
                    Relationship.RelationshipType.CONNECTS_TO
                ),
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_filter_relationships_by_organization(self):
        Relationship.objects.create(
            source=self.web,
            target=self.api,
            relationship_type=(
                Relationship.RelationshipType.CONNECTS_TO
            ),
        )

        response = self.client.get(
            reverse("relationship-list"),
            {
                "organization": self.organization.pk,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )
