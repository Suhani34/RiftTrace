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


class RiftTraceEndToEndTests(
    APITestCase
):
    def setUp(self):
        self.organization = (
            Organization.objects.create(
                name="EndToEndCorp"
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

                reference_id=(
                    "E2E-001"
                ),

                title=(
                    "Modeled API weakness"
                ),

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

                bypasses_mfa=False,

                is_exploitable=True,
            )
        )


        self.process = (
            BusinessProcess.objects.create(
                organization=(
                    self.organization
                ),

                name="Customer Service",

                criticality=(
                    BusinessProcess
                    .Criticality
                    .CRITICAL
                ),

                impact_description=(
                    "Customer service could "
                    "potentially be affected."
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


        self.control = (
            SecurityControl.objects.create(
                organization=(
                    self.organization
                ),

                name=(
                    "Segment Web from API"
                ),

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


    def test_complete_rifttrace_workflow(
        self,
    ):
        propagation_response = (
            self.client.post(
                reverse(
                    "simulation-attack-propagation"
                ),

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
        )


        self.assertEqual(
            propagation_response
            .status_code,

            status.HTTP_200_OK,
        )


        self.assertIn(
            self.api.id,

            propagation_response.data[
                "propagated_asset_ids"
            ],
        )


        business_response = (
            self.client.post(
                reverse(
                    "simulation-business-impact"
                ),

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
        )


        self.assertEqual(
            business_response
            .status_code,

            status.HTTP_200_OK,
        )


        self.assertEqual(
            business_response.data[
                "business_impact"
            ][
                "summary"
            ][
                "critical_process_count"
            ],

            1,
        )


        control_response = (
            self.client.post(
                reverse(
                    "simulation-security-controls"
                ),

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
        )


        self.assertEqual(
            control_response.status_code,

            status.HTTP_200_OK,
        )


        self.assertEqual(
            control_response.data[
                "comparison"
            ][
                "propagated_asset_reduction"
            ],

            1,
        )


        ranking_response = (
            self.client.post(
                reverse(
                    "simulation-control-ranking"
                ),

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
        )


        self.assertEqual(
            ranking_response.status_code,

            status.HTTP_200_OK,
        )


        self.assertEqual(
            ranking_response.data[
                "ranked_controls"
            ][
                0
            ][
                "rank"
            ],

            1,
        )
