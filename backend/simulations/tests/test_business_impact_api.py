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
    Vulnerability,
)


class BusinessImpactSimulationAPITests(
    APITestCase
):
    def setUp(self):
        self.organization = (
            Organization.objects.create(
                name="ImpactCorp"
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

                is_internet_exposed=True,
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
                    .HIGH
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

            required_source_privilege=(
                Relationship
                .RequiredSourcePrivilege
                .LOW
            ),
        )


        Vulnerability.objects.create(
            asset=self.api,

            reference_id="TEST-API-001",

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

                impact_description=(
                    "Checkout may be affected."
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


        self.url = reverse(
            "simulation-business-impact"
        )


    def test_business_process_is_impacted(
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


        summary = (
            response.data[
                "business_impact"
            ][
                "summary"
            ]
        )


        self.assertEqual(
            summary[
                "impacted_process_count"
            ],
            1,
        )


        self.assertEqual(
            summary[
                "critical_process_count"
            ],
            1,
        )


        impacted = (
            response.data[
                "business_impact"
            ][
                "impacted_processes"
            ]
        )


        self.assertEqual(
            impacted[0][
                "business_process"
            ][
                "name"
            ],
            "Checkout",
        )
