from django.urls import reverse

from rest_framework import status
from rest_framework.test import (
    APITestCase,
)

from assets.models import Asset

from organizations.models import (
    Organization,
)


class DashboardSummaryAPITests(
    APITestCase
):
    def setUp(self):
        self.organization = (
            Organization.objects.create(
                name="DashboardCorp"
            )
        )


        Asset.objects.create(
            organization=(
                self.organization
            ),

            name="Critical API",

            asset_type=(
                Asset.AssetType.API
            ),

            criticality=(
                Asset
                .Criticality
                .CRITICAL
            ),
        )


        self.url = reverse(
            "dashboard-summary"
        )


    def test_dashboard_summary(
        self,
    ):
        response = self.client.get(
            self.url,

            {
                "organization":
                    self.organization.id
            },
        )


        self.assertEqual(
            response.status_code,

            status.HTTP_200_OK,
        )


        self.assertEqual(
            response.data[
                "totals"
            ][
                "assets"
            ],

            1,
        )


    def test_organization_required(
        self,
    ):
        response = self.client.get(
            self.url
        )


        self.assertEqual(
            response.status_code,

            status
            .HTTP_400_BAD_REQUEST,
        )
