from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Organization


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
