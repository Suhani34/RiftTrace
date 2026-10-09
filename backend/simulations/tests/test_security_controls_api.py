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
    SecurityControl,
    Vulnerability,
)


class SecurityControlSimulationAPITests(
    APITestCase
):
    def setUp(self):
        self.organization = (
            Organization.objects.create(
                name="ControlSimulationCorp"
            )
        )


        self.web = (
            Asset.objects.create(
                organization=(
                    self.organization
                ),

                name="Web",

                asset_type=(
                    Asset
                    .AssetType
                    .APPLICATION
                ),
            )
        )


        self.api = (
            Asset.objects.create(
                organization=(
                    self.organization
                ),

                name="API",

                asset_type=(
                    Asset.AssetType.API
                ),

                criticality=(
                    Asset
                    .Criticality
                    .CRITICAL
                ),
            )
        )


        self.relationship = (
            Relationship.objects.create(
                source=self.web,

                target=self.api,

                relationship_type=(
                    Relationship
                    .RelationshipType
                    .CALLS
                ),

                required_source_privilege=(
                    Relationship
                    .RequiredSourcePrivilege
                    .LOW
                ),
            )
        )


        self.vulnerability = (
            Vulnerability.objects.create(
                asset=self.api,

                title="API weakness",

                attack_vector=(
                    Vulnerability
                    .AttackVector
                    .NETWORK
                ),

                privileges_required=(
                    Vulnerability
                    .PrivilegesRequired
                    .NONE
                ),

                grants_privilege=(
                    Vulnerability
                    .GrantedPrivilege
                    .LOW
                ),

                is_exploitable=True,
            )
        )


        self.control = (
            SecurityControl.objects.create(
                organization=(
                    self.organization
                ),

                name="Segment Web API",

                control_type=(
                    SecurityControl
                    .ControlType
                    .NETWORK_SEGMENTATION
                ),

                target_relationship=(
                    self.relationship
                ),
            )
        )


        self.url = reverse(
            "simulation-security-controls"
        )


    def test_segmentation_control_reduces_propagation_without_deleting_relationship(
        self,
    ):
        response = self.client.post(
            self.url,

            {
                "organization":
                    self.organization.id,

                "start_asset":
                    self.web.id,

                "start_privilege":
                    "LOW",

                "control_ids": [
                    self.control.id
                ],
            },

            format="json",
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


        self.assertEqual(
            response.data[
                "baseline"
            ][
                "technical_consequence"
            ][
                "propagated_asset_count"
            ],
            1,
        )


        self.assertEqual(
            response.data[
                "counterfactual"
            ][
                "technical_consequence"
            ][
                "propagated_asset_count"
            ],
            0,
        )


        self.assertTrue(
            Relationship.objects.filter(
                id=self.relationship.id
            ).exists()
        )
