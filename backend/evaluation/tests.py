from rest_framework import status
from rest_framework.test import APITestCase

from organizations.models import (
    Organization,
)

from scenarios.models import (
    SavedScenario,
    ScenarioRun,
)

from .models import (
    EvaluationExperiment,
)


class EvaluationApiTests(
    APITestCase
):
    def setUp(
        self,
    ):
        self.organization = (
            Organization.objects.create(
                name=(
                    "Phase 18 Test Organization"
                )
            )
        )


        self.scenario = (
            SavedScenario.objects.create(
                organization=(
                    self.organization
                ),

                name=(
                    "MFA Evaluation Scenario"
                ),

                simulation_type=(
                    SavedScenario
                    .SimulationType
                    .IDENTITY_PROPAGATION
                ),

                request_payload={
                    "organization":
                        self.organization.id,
                },
            )
        )


        self.baseline_run = (
            ScenarioRun.objects.create(
                scenario=(
                    self.scenario
                ),

                run_number=1,

                label=(
                    "Before MFA"
                ),

                status=(
                    ScenarioRun.Status.SUCCESS
                ),

                metrics={
                    "compromised_assets":
                        6,

                    "acquired_identities":
                        4,
                },
            )
        )


        self.treatment_run = (
            ScenarioRun.objects.create(
                scenario=(
                    self.scenario
                ),

                run_number=2,

                label=(
                    "After MFA"
                ),

                status=(
                    ScenarioRun.Status.SUCCESS
                ),

                metrics={
                    "compromised_assets":
                        3,

                    "acquired_identities":
                        2,
                },
            )
        )


    def test_create_experiment(
        self,
    ):
        response = self.client.post(
            "/api/evaluation/experiments/",

            {
                "organization":
                    self.organization.id,

                "name":
                    "MFA Experiment",

                "scenario":
                    self.scenario.id,

                "baseline_run":
                    self.baseline_run.id,

                "treatment_run":
                    self.treatment_run.id,

                "intervention_label":
                    "Require MFA",

                "notes":
                    "Phase 18 automated test",
            },

            format="json",
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )


        self.assertEqual(
            response.data[
                "comparison"
            ][0][
                "interpretation"
            ],
            "IMPROVED",
        )


    def test_reject_reversed_runs(
        self,
    ):
        response = self.client.post(
            "/api/evaluation/experiments/",

            {
                "organization":
                    self.organization.id,

                "name":
                    "Invalid Experiment",

                "scenario":
                    self.scenario.id,

                "baseline_run":
                    self.treatment_run.id,

                "treatment_run":
                    self.baseline_run.id,

                "intervention_label":
                    "Invalid chronology",
            },

            format="json",
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )


    def test_evaluation_summary(
        self,
    ):
        EvaluationExperiment.objects.create(
            organization=(
                self.organization
            ),

            name=(
                "MFA Experiment"
            ),

            scenario=(
                self.scenario
            ),

            baseline_run=(
                self.baseline_run
            ),

            treatment_run=(
                self.treatment_run
            ),

            intervention_label=(
                "Require MFA"
            ),
        )


        response = self.client.get(
            (
                "/api/evaluation/summary/"
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
                "experiment_count"
            ],
            1,
        )


        self.assertEqual(
            response.data[
                "improved_observations"
            ],
            2,
        )


    def test_csv_export(
        self,
    ):
        EvaluationExperiment.objects.create(
            organization=(
                self.organization
            ),

            name=(
                "MFA Experiment"
            ),

            scenario=(
                self.scenario
            ),

            baseline_run=(
                self.baseline_run
            ),

            treatment_run=(
                self.treatment_run
            ),

            intervention_label=(
                "Require MFA"
            ),
        )


        response = self.client.get(
            (
                "/api/evaluation/export.csv"
                f"?organization="
                f"{self.organization.id}"
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
            response.content.decode(
                "utf-8"
            )
        )


        self.assertIn(
            "MFA Experiment",
            content,
        )


        self.assertIn(
            "compromised_assets",
            content,
        )
