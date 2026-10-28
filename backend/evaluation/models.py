from django.core.exceptions import ValidationError
from django.db import models

from organizations.models import Organization
from scenarios.models import (
    SavedScenario,
    ScenarioRun,
)


class EvaluationExperiment(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="evaluation_experiments",
    )

    name = models.CharField(
        max_length=200,
    )

    scenario = models.ForeignKey(
        SavedScenario,
        on_delete=models.PROTECT,
        related_name="evaluation_experiments",
    )

    baseline_run = models.ForeignKey(
        ScenarioRun,
        on_delete=models.PROTECT,
        related_name="baseline_evaluations",
    )

    treatment_run = models.ForeignKey(
        ScenarioRun,
        on_delete=models.PROTECT,
        related_name="treatment_evaluations",
    )

    intervention_label = models.CharField(
        max_length=250,
    )

    notes = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )


    class Meta:
        ordering = (
            "-created_at",
            "-id",
        )

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "organization",
                    "name",
                ),

                name=(
                    "unique_evaluation_name_per_org"
                ),
            ),
        ]


    def clean(self):
        errors = {}


        if (
            self.scenario_id
            and self.organization_id
            and (
                self.scenario.organization_id
                != self.organization_id
            )
        ):
            errors["scenario"] = (
                "The scenario must belong "
                "to the selected organization."
            )


        if (
            self.baseline_run_id
            and self.scenario_id
            and (
                self.baseline_run.scenario_id
                != self.scenario_id
            )
        ):
            errors["baseline_run"] = (
                "The baseline run must belong "
                "to the selected scenario."
            )


        if (
            self.treatment_run_id
            and self.scenario_id
            and (
                self.treatment_run.scenario_id
                != self.scenario_id
            )
        ):
            errors["treatment_run"] = (
                "The treatment run must belong "
                "to the selected scenario."
            )


        if (
            self.baseline_run_id
            and self.treatment_run_id
            and (
                self.baseline_run_id
                == self.treatment_run_id
            )
        ):
            errors["treatment_run"] = (
                "Baseline and treatment runs "
                "must be different."
            )


        if (
            self.baseline_run_id
            and (
                self.baseline_run.status
                != ScenarioRun.Status.SUCCESS
            )
        ):
            errors["baseline_run"] = (
                "The baseline run must "
                "be successful."
            )


        if (
            self.treatment_run_id
            and (
                self.treatment_run.status
                != ScenarioRun.Status.SUCCESS
            )
        ):
            errors["treatment_run"] = (
                "The treatment run must "
                "be successful."
            )


        if (
            self.baseline_run_id
            and self.treatment_run_id
            and (
                self.baseline_run.run_number
                >= self.treatment_run.run_number
            )
        ):
            errors["treatment_run"] = (
                "The treatment run must occur "
                "after the baseline run."
            )


        if errors:
            raise ValidationError(
                errors
            )


    def save(
        self,
        *args,
        **kwargs,
    ):
        self.full_clean()

        super().save(
            *args,
            **kwargs,
        )


    def __str__(self):
        return (
            f"{self.organization.name}"
            f" - {self.name}"
        )
