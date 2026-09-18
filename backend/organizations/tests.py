from django.test import TestCase

from .models import Organization


class OrganizationModelTests(TestCase):
    def test_organization_string_representation(self):
        organization = Organization.objects.create(
            name="DemoCorp"
        )

        self.assertEqual(
            str(organization),
            "DemoCorp",
        )
