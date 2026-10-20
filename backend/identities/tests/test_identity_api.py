from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from assets.models import Asset
from organizations.models import Organization

from identities.models import (
    CredentialExposure,
    Identity,
    IdentityAccess,
)


class IdentityPropagationAPITests(
    APITestCase
):
    def setUp(self):
        self.organization = (
            Organization.objects.create(
                name="Identity Test Corp"
            )
        )


        self.source_asset = (
            Asset.objects.create(
                organization=self.organization,

                name="Source Asset",

                asset_type="SERVER",

                criticality="HIGH",

                environment="PRODUCTION",
            )
        )


        self.target_asset = (
            Asset.objects.create(
                organization=self.organization,

                name="Target Asset",

                asset_type="SERVER",

                criticality="CRITICAL",

                environment="PRODUCTION",
            )
        )


        self.identity = (
            Identity.objects.create(
                organization=self.organization,

                name="test-user",

                identity_type=(
                    Identity
                    .IdentityType
                    .USER
                ),

                privilege_level=(
                    Identity
                    .PrivilegeLevel
                    .LOW
                ),
            )
        )


        CredentialExposure.objects.create(
            organization=self.organization,

            name="Test Credential",

            identity=self.identity,

            stored_on_asset=(
                self.source_asset
            ),

            credential_type=(
                CredentialExposure
                .CredentialType
                .PASSWORD
            ),

            discoverable_on_compromise=True,

            satisfies_mfa=False,

            active=True,
        )


        IdentityAccess.objects.create(
            organization=self.organization,

            identity=self.identity,

            asset=self.target_asset,

            access_type=(
                IdentityAccess
                .AccessType
                .LOGIN
            ),

            granted_privilege="LOW",

            requires_mfa=False,

            enabled=True,
        )


    def test_identity_propagation_reaches_target(
        self,
    ):
        response = self.client.post(
            reverse(
                "identity-propagation"
            ),

            {
                "organization":
                    self.organization.id,

                "compromised_assets": [
                    {
                        "asset_id":
                            self.source_asset.id,

                        "privilege":
                            "LOW",
                    }
                ],
            },

            format="json",
        )


        self.assertEqual(
            response.status_code,

            status.HTTP_200_OK,
        )


        reached_ids = {
            item[
                "asset_id"
            ]

            for item
            in response.data[
                "compromised_assets"
            ]
        }


        self.assertIn(
            self.target_asset.id,

            reached_ids,
        )
