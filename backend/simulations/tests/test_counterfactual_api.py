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


class CounterfactualSimulationAPITests(
    APITestCase
):
    def setUp(self):
        self.organization = (
            Organization.objects.create(
                name="CounterfactualCorp"
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

                protocol="HTTPS",

                port=443,

                requires_authentication=True,

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

                reference_id="CF-001",

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


        self.url = reverse(
            "simulation-counterfactual"
        )


    def test_disabling_relationship_changes_result_without_deleting_relationship(
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

                "disabled_relationship_ids":
                    [
                        self.relationship.id
                    ],

                "disabled_vulnerability_ids":
                    [],
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


    def test_disabling_vulnerability_does_not_change_database_record(
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

                "disabled_relationship_ids":
                    [],

                "disabled_vulnerability_ids":
                    [
                        self.vulnerability.id
                    ],
            },

            format="json",
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


        self.vulnerability.refresh_from_db()


        self.assertTrue(
            self.vulnerability
            .is_exploitable
        )


    def test_no_modification_is_rejected(
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

                "disabled_relationship_ids":
                    [],

                "disabled_vulnerability_ids":
                    [],
            },

            format="json",
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

