from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from assets.models import (
    Asset,
    NetworkZone,
    Relationship,
)

from organizations.models import (
    Organization,
)


class ReachabilitySimulationAPITests(
    APITestCase
):
    def setUp(self):
        self.organization = (
            Organization.objects.create(
                name="SimulationCorp"
            )
        )


        self.other_organization = (
            Organization.objects.create(
                name="OtherSimulationCorp"
            )
        )


        self.zone = (
            NetworkZone.objects.create(
                organization=(
                    self.organization
                ),

                name="Internal",

                zone_type=(
                    NetworkZone
                    .ZoneType
                    .INTERNAL
                ),
            )
        )


        self.other_zone = (
            NetworkZone.objects.create(
                organization=(
                    self.other_organization
                ),

                name="Other Internal",

                zone_type=(
                    NetworkZone
                    .ZoneType
                    .INTERNAL
                ),
            )
        )


        self.web = Asset.objects.create(
            organization=self.organization,

            name="Web",

            asset_type=(
                Asset
                .AssetType
                .APPLICATION
            ),

            criticality=(
                Asset
                .Criticality
                .HIGH
            ),

            network_zone=self.zone,

            is_internet_exposed=True,
        )


        self.api = Asset.objects.create(
            organization=self.organization,

            name="API",

            asset_type=(
                Asset.AssetType.API
            ),

            criticality=(
                Asset
                .Criticality
                .HIGH
            ),

            network_zone=self.zone,
        )


        self.database = (
            Asset.objects.create(
                organization=(
                    self.organization
                ),

                name="Database",

                asset_type=(
                    Asset
                    .AssetType
                    .DATABASE
                ),

                criticality=(
                    Asset
                    .Criticality
                    .CRITICAL
                ),

                network_zone=self.zone,
            )
        )


        self.isolated = (
            Asset.objects.create(
                organization=(
                    self.organization
                ),

                name="Isolated",

                asset_type=(
                    Asset
                    .AssetType
                    .SERVER
                ),

                network_zone=self.zone,
            )
        )


        self.foreign_asset = (
            Asset.objects.create(
                organization=(
                    self.other_organization
                ),

                name="Foreign Asset",

                asset_type=(
                    Asset
                    .AssetType
                    .SERVER
                ),

                network_zone=(
                    self.other_zone
                ),
            )
        )


        Relationship.objects.create(
            source=self.web,
            target=self.api,

            relationship_type=(
                Relationship
                .RelationshipType
                .CALLS
            ),

            protocol="HTTPS",
            port=443,
            requires_authentication=True,
        )


        Relationship.objects.create(
            source=self.api,
            target=self.database,

            relationship_type=(
                Relationship
                .RelationshipType
                .READS
            ),

            protocol="TCP",
            port=5432,
            requires_authentication=True,
        )


        self.url = reverse(
            "simulation-reachability"
        )


    def test_reachability_simulation(
        self,
    ):
        response = self.client.post(
            self.url,

            {
                "organization":
                    self.organization.id,

                "start_asset":
                    self.web.id,
            },

            format="json",
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


        self.assertEqual(
            response.data[
                "summary"
            ][
                "reachable_asset_count"
            ],
            2,
        )


        self.assertEqual(
            response.data[
                "summary"
            ][
                "reachable_critical_asset_count"
            ],
            1,
        )


        self.assertEqual(
            response.data[
                "summary"
            ][
                "max_hops"
            ],
            2,
        )


        self.assertEqual(
            set(
                response.data[
                    "reachable_asset_ids"
                ]
            ),
            {
                self.api.id,
                self.database.id,
            },
        )


    def test_foreign_start_asset_is_rejected(
        self,
    ):
        response = self.client.post(
            self.url,

            {
                "organization":
                    self.organization.id,

                "start_asset":
                    self.foreign_asset.id,
            },

            format="json",
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )


    def test_isolated_asset_returns_zero_reachable(
        self,
    ):
        response = self.client.post(
            self.url,

            {
                "organization":
                    self.organization.id,

                "start_asset":
                    self.isolated.id,
            },

            format="json",
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


        self.assertEqual(
            response.data[
                "summary"
            ][
                "reachable_asset_count"
            ],
            0,
        )


        self.assertEqual(
            response.data[
                "summary"
            ][
                "max_hops"
            ],
            0,
        )
