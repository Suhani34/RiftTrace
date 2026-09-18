from django.core.exceptions import ValidationError
from django.test import TestCase

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
