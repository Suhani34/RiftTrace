import json

from django.core.files.uploadedfile import (
    SimpleUploadedFile,
)

from django.urls import reverse

from rest_framework import status

from rest_framework.test import (
    APITestCase,
)

from assets.models import (
    Asset,
    Relationship,
)

from organizations.models import (
    Organization,
)

from security.models import (
    Vulnerability,
)

from ingestion.models import (
    IngestionRun,
)


class IngestionAPITests(
    APITestCase
):
    def setUp(self):
        self.organization = (
            Organization.objects.create(
                name="ImportTestCorp"
            )
        )


        self.preview_url = reverse(
            "ingestion-preview"
        )


        self.apply_url = reverse(
            "ingestion-apply"
        )


    def make_bundle(
        self,
    ):
        return {
            "network_zones": [
                {
                    "name":
                        "Test DMZ",

                    "zone_type":
                        "DMZ",
                }
            ],

            "assets": [
                {
                    "name":
                        "Test Web",

                    "asset_type":
                        "APPLICATION",

                    "criticality":
                        "HIGH",

                    "environment":
                        "PRODUCTION",

                    "network_zone":
                        "Test DMZ",

                    "hostname":
                        "test-web",

                    "ip_address":
                        "10.99.1.10",

                    "is_internet_exposed":
                        True,
                },

                {
                    "name":
                        "Test API",

                    "asset_type":
                        "API",

                    "criticality":
                        "CRITICAL",

                    "environment":
                        "PRODUCTION",

                    "network_zone":
                        "Test DMZ",

                    "hostname":
                        "test-api",

                    "ip_address":
                        "10.99.1.20",

                    "is_internet_exposed":
                        False,
                },
            ],

            "relationships": [
                {
                    "source":
                        "Test Web",

                    "target":
                        "Test API",

                    "relationship_type":
                        "CALLS",

                    "protocol":
                        "HTTPS",

                    "port":
                        443,

                    "requires_authentication":
                        True,

                    "required_source_privilege":
                        "LOW",
                }
            ],

            "vulnerabilities": [
                {
                    "asset":
                        "Test API",

                    "reference_id":
                        "TEST-IMPORT-001",

                    "title":
                        "Test API vulnerability",

                    "cvss_score":
                        8.0,

                    "attack_vector":
                        "NETWORK",

                    "privileges_required":
                        "NONE",

                    "grants_privilege":
                        "LOW",

                    "bypasses_authentication":
                        True,

                    "bypasses_mfa":
                        False,

                    "is_exploitable":
                        True,

                    "description":
                        "Test vulnerability.",
                }
            ],
        }


    def make_file(
        self,
        bundle=None,
    ):
        if bundle is None:
            bundle = (
                self.make_bundle()
            )


        return SimpleUploadedFile(
            "bundle.json",

            json.dumps(
                bundle
            ).encode(
                "utf-8"
            ),

            content_type=(
                "application/json"
            ),
        )


    def test_preview_does_not_modify_database(
        self,
    ):
        response = self.client.post(
            self.preview_url,

            {
                "organization":
                    self.organization.id,

                "source_format":
                    "JSON",

                "bundle_file":
                    self.make_file(),
            },

            format="multipart",
        )


        self.assertEqual(
            response.status_code,

            status.HTTP_200_OK,
        )


        self.assertTrue(
            response.data[
                "valid"
            ]
        )


        self.assertEqual(
            Asset.objects.filter(
                organization=(
                    self.organization
                )
            ).count(),

            0,
        )


    def test_apply_creates_environment(
        self,
    ):
        response = self.client.post(
            self.apply_url,

            {
                "organization":
                    self.organization.id,

                "source_format":
                    "JSON",

                "bundle_file":
                    self.make_file(),
            },

            format="multipart",
        )


        self.assertEqual(
            response.status_code,

            status
            .HTTP_201_CREATED,
        )


        self.assertEqual(
            Asset.objects.filter(
                organization=(
                    self.organization
                )
            ).count(),

            2,
        )


        self.assertEqual(
            Relationship.objects.filter(
                source__organization=(
                    self.organization
                )
            ).count(),

            1,
        )


        self.assertEqual(
            Vulnerability.objects.filter(
                asset__organization=(
                    self.organization
                )
            ).count(),

            1,
        )


        self.assertEqual(
            IngestionRun.objects.filter(
                organization=(
                    self.organization
                )
            ).count(),

            1,
        )


    def test_repeat_import_does_not_duplicate_records(
        self,
    ):
        for _ in range(2):
            response = self.client.post(
                self.apply_url,

                {
                    "organization":
                        self.organization.id,

                    "source_format":
                        "JSON",

                    "bundle_file":
                        self.make_file(),
                },

                format="multipart",
            )


            self.assertEqual(
                response.status_code,

                status
                .HTTP_201_CREATED,
            )


        self.assertEqual(
            Asset.objects.filter(
                organization=(
                    self.organization
                )
            ).count(),

            2,
        )


        self.assertEqual(
            Relationship.objects.filter(
                source__organization=(
                    self.organization
                )
            ).count(),

            1,
        )


        self.assertEqual(
            Vulnerability.objects.filter(
                asset__organization=(
                    self.organization
                )
            ).count(),

            1,
        )


    def test_invalid_reference_is_not_applied(
        self,
    ):
        bundle = self.make_bundle()


        bundle[
            "relationships"
        ][
            0
        ][
            "target"
        ] = "Missing Database"


        response = self.client.post(
            self.apply_url,

            {
                "organization":
                    self.organization.id,

                "source_format":
                    "JSON",

                "bundle_file":
                    self.make_file(
                        bundle
                    ),
            },

            format="multipart",
        )


        self.assertEqual(
            response.status_code,

            status
            .HTTP_400_BAD_REQUEST,
        )


        self.assertEqual(
            Asset.objects.filter(
                organization=(
                    self.organization
                )
            ).count(),

            0,
        )
