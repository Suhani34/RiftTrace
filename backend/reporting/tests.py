from rest_framework import status
from rest_framework.test import APITestCase

from organizations.models import (
    Organization,
)

from scenarios.models import (
    SavedScenario,
    ScenarioRun,
)


class ReportingApiTests(
    APITestCase
):
    def setUp(
        self,
    ):
        self.organization = (
            Organization.objects.create(
                name=(
                    "Reporting Test Org"
                ),

                description=(
                    "Phase 20 automated test."
                ),
            )
        )


        self.scenario = (
            SavedScenario.objects.create(
                organization=(
                    self.organization
                ),

                name=(
                    "Reporting Test Scenario"
                ),

                simulation_type=(
                    SavedScenario
                    .SimulationType
                    .IDENTITY_PROPAGATION
                ),

                description=(
                    "Machine-readable "
                    "report test."
                ),

                request_payload={
                    "organization":
                        self.organization.id,

                    "compromised_assets": [],
                },
            )
        )


        self.run = (
            ScenarioRun.objects.create(
                scenario=(
                    self.scenario
                ),

                run_number=1,

                label=(
                    "Baseline"
                ),

                status=(
                    ScenarioRun
                    .Status
                    .SUCCESS
                ),

                request_payload={
                    "organization":
                        self.organization.id,
                },

                result_payload={
                    "compromised_assets": [
                        1,
                        2,
                        3,
                    ]
                },

                metrics={
                    "compromised_assets":
                        3,

                    "acquired_identities":
                        2,
                },

                error_message="",
            )
        )


    def test_reporting_summary(
        self,
    ):
        response = self.client.get(
            (
                "/api/reporting/summary/"
                f"?organization="
                f"{self.organization.id}"
            )
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


        self.assertEqual(
            response.data[
                "scenarios"
            ][
                "total"
            ],
            1,
        )


    def test_environment_export(
        self,
    ):
        response = self.client.get(
            (
                "/api/reporting/"
                f"environment/"
                f"{self.organization.id}/"
            )
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


        self.assertIn(
            b"rifttrace.environment",
            response.content,
        )


    def test_ingestion_environment_export(
        self,
    ):
        response = self.client.get(
            (
                "/api/reporting/"
                f"environment/"
                f"{self.organization.id}/"
                "ingestion/"
            )
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


        self.assertIn(
            b'"assets"',
            response.content,
        )


    def test_scenario_export(
        self,
    ):
        response = self.client.get(
            (
                "/api/reporting/"
                f"scenarios/"
                f"{self.scenario.id}/"
            )
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


        self.assertIn(
            b"Reporting Test Scenario",
            response.content,
        )


        self.assertIn(
            b'"runs"',
            response.content,
        )


    def test_run_report(
        self,
    ):
        response = self.client.get(
            (
                "/api/reporting/"
                f"runs/"
                f"{self.run.id}/"
            )
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


        self.assertIn(
            (
                b"rifttrace."
                b"simulation-run-report"
            ),
            response.content,
        )


        self.assertIn(
            b"compromised_assets",
            response.content,
        )


    def test_run_metrics_csv(
        self,
    ):
        response = self.client.get(
            (
                "/api/reporting/"
                f"runs/"
                f"{self.run.id}/"
                "metrics.csv"
            )
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


        self.assertEqual(
            response[
                "Content-Type"
            ],
            "text/csv",
        )


        content = (
            response
            .content
            .decode(
                "utf-8"
            )
        )


        self.assertIn(
            "compromised_assets",
            content,
        )


        self.assertIn(
            "acquired_identities",
            content,
        )
