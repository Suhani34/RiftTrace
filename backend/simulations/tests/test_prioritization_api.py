from django.urls import reverse

from rest_framework import status
from rest_framework.test import (
    APITestCase,
)

from assets.models import (
    Asset,
    Relationship,
)

from business.models import (
    BusinessProcess,
    BusinessProcessDependency,
)

from organizations.models import (
    Organization,
)

from security.models import (
    SecurityControl,
    Vulnerability,
)


class PrioritizationAPITests(
    APITestCase
):
    def setUp(self):
        self.organization = (
            Organization.objects.create(
                name="RankingCorp"
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

                criticality=(
                    Asset
                    .Criticality
                    .HIGH
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

                bypasses_authentication=True,

                is_exploitable=True,

                bypasses_mfa=False,
            )
        )


        self.process = (
            BusinessProcess.objects.create(
                organization=(
                    self.organization
                ),

                name="Checkout",

                criticality=(
                    BusinessProcess
                    .Criticality
                    .CRITICAL
                ),
            )
        )


        (
            BusinessProcessDependency
            .objects
            .create(
                business_process=(
                    self.process
                ),

                asset=self.api,

                dependency_level=(
                    BusinessProcessDependency
                    .DependencyLevel
                    .ESSENTIAL
                ),
            )
        )


        self.segmentation = (
            SecurityControl.objects.create(
                organization=(
                    self.organization
                ),

                name="Segment path",

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


        self.authentication = (
            SecurityControl.objects.create(
                organization=(
                    self.organization
                ),

                name="Require authentication",

                control_type=(
                    SecurityControl
                    .ControlType
                    .AUTHENTICATION_ENFORCEMENT
                ),

                target_relationship=(
                    self.relationship
                ),
            )
        )


        self.url = reverse(
            "simulation-control-ranking"
        )


    def test_effective_control_ranks_above_zero_effect_control(
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
            },

            format="json",
        )


        self.assertEqual(
            response.status_code,

            status.HTTP_200_OK,
        )


        ranking = {
            item[
                "control"
            ][
                "id"
            ]:
                item

            for item
            in response.data[
                "ranked_controls"
            ]
        }


        self.assertLess(
            ranking[
                self.segmentation.id
            ][
                "rank"
            ],

            ranking[
                self.authentication.id
            ][
                "rank"
            ],
        )


        self.assertTrue(
            ranking[
                self.segmentation.id
            ][
                "has_measured_effect"
            ]
        )


        self.assertFalse(
            ranking[
                self.authentication.id
            ][
                "has_measured_effect"
            ]
        )


    def test_candidate_count_matches_controls(
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
            },

            format="json",
        )


        self.assertEqual(
            response.data[
                "candidate_control_count"
            ],

            2,
        )
