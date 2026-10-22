from rest_framework import status
from rest_framework.test import APITestCase

from organizations.models import Organization

from .models import (
    SavedScenario,
    ScenarioRun,
)


class ScenarioHistoryApiTests(
    APITestCase
):
    def setUp(
        self,
    ):
        self.organization = (
            Organization.objects.create(
                name=(
                    "Phase 17 Test Organization"
                )
            )
        )


        self.scenario = (
            SavedScenario.objects.create(
                organization=(
                    self.organization
                ),

                name=(
                    "Identity Baseline"
                ),

                simulation_type=(
                    SavedScenario
                    .SimulationType
                    .IDENTITY_PROPAGATION
                ),

                description=(
                    "Phase 17 test scenario"
                ),

                request_payload={
                    "organization":
                        self.organization.id,

                    "compromised_assets": [
                        {
                            "asset_id":
                                1,

                            "privilege":
                                "LOW",
                        }
                    ],
                },
            )
        )


    def test_create_scenario(
        self,
    ):
        response = self.client.post(
            "/api/scenarios/",

            {
                "organization":
                    self.organization.id,

                "name":
                    "Second Scenario",

                "simulation_type":
                    "REACHABILITY",

                "description":
                    "Another saved experiment",

                "request_payload": {
                    "organization":
                        self.organization.id,
                },
            },

            format="json",
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data[
                "name"
            ],
            "Second Scenario",
        )


    def test_run_numbers_increment(
        self,
    ):
        first_response = (
            self.client.post(
                (
                    f"/api/scenarios/"
                    f"{self.scenario.id}/runs/"
                ),

                {
                    "label":
                        "Before MFA",

                    "status":
                        "SUCCESS",

                    "result_payload": {
                        "example":
                            True,
                    },

                    "metrics": {
                        "compromised_assets":
                            6,

                        "acquired_identities":
                            4,
                    },
                },

                format="json",
            )
        )


        second_response = (
            self.client.post(
                (
                    f"/api/scenarios/"
                    f"{self.scenario.id}/runs/"
                ),

                {
                    "label":
                        "After MFA",

                    "status":
                        "SUCCESS",

                    "result_payload": {
                        "example":
                            True,
                    },

                    "metrics": {
                        "compromised_assets":
                            3,

                        "acquired_identities":
                            2,
                    },
                },

                format="json",
            )
        )


        self.assertEqual(
            first_response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            second_response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            first_response.data[
                "run_number"
            ],
            1,
        )

        self.assertEqual(
            second_response.data[
                "run_number"
            ],
            2,
        )


    def test_compare_runs(
        self,
    ):
        before_run = (
            ScenarioRun.objects.create(
                scenario=(
                    self.scenario
                ),

                run_number=1,

                status="SUCCESS",

                metrics={
                    "compromised_assets":
                        6,

                    "acquired_identities":
                        4,
                },
            )
        )


        after_run = (
            ScenarioRun.objects.create(
                scenario=(
                    self.scenario
                ),

                run_number=2,

                status="SUCCESS",

                metrics={
                    "compromised_assets":
                        3,

                    "acquired_identities":
                        2,
                },
            )
        )


        response = self.client.get(
            (
                f"/api/scenarios/"
                f"{self.scenario.id}/compare/"
                f"?before_run={before_run.id}"
                f"&after_run={after_run.id}"
            )
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


        metrics = {
            item["metric"]:
                item

            for item
            in response.data[
                "metrics"
            ]
        }


        self.assertEqual(
            metrics[
                "compromised_assets"
            ][
                "reduction"
            ],
            3,
        )


        self.assertEqual(
            metrics[
                "acquired_identities"
            ][
                "reduction"
            ],
            2,
        )


        self.assertEqual(
            metrics[
                "compromised_assets"
            ][
                "interpretation"
            ],
            "IMPROVED",
        )


    def test_failed_run_requires_message(
        self,
    ):
        response = self.client.post(
            (
                f"/api/scenarios/"
                f"{self.scenario.id}/runs/"
            ),

            {
                "status":
                    "FAILED",

                "metrics":
                    {},
            },

            format="json",
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
