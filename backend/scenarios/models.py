from django.db import models

from organizations.models import Organization


class SavedScenario(models.Model):
    class SimulationType(models.TextChoices):
        REACHABILITY = (
            "REACHABILITY",
            "Reachability",
        )

        ATTACK_PROPAGATION = (
            "ATTACK_PROPAGATION",
            "Attack Propagation",
        )

        BUSINESS_IMPACT = (
            "BUSINESS_IMPACT",
            "Business Impact",
        )

        COUNTERFACTUAL = (
            "COUNTERFACTUAL",
            "Counterfactual",
        )

        SECURITY_CONTROL = (
            "SECURITY_CONTROL",
            "Security Control",
        )

        CONTROL_RANKING = (
            "CONTROL_RANKING",
            "Control Ranking",
        )

        IDENTITY_PROPAGATION = (
            "IDENTITY_PROPAGATION",
            "Identity Propagation",
        )


    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="saved_scenarios",
    )

    name = models.CharField(
        max_length=200,
    )

    simulation_type = models.CharField(
        max_length=40,
        choices=SimulationType.choices,
    )

    description = models.TextField(
        blank=True,
    )

    request_payload = models.JSONField(
        default=dict,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )


    class Meta:
        ordering = (
            "-updated_at",
            "-id",
        )

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "organization",
                    "name",
                ),

                name=(
                    "unique_saved_scenario_name_per_org"
                ),
            ),
        ]


    def __str__(self):
        return (
            f"{self.organization.name}"
            f" - {self.name}"
        )


class ScenarioRun(models.Model):
    class Status(models.TextChoices):
        SUCCESS = (
            "SUCCESS",
            "Success",
        )

        FAILED = (
            "FAILED",
            "Failed",
        )


    scenario = models.ForeignKey(
        SavedScenario,
        on_delete=models.CASCADE,
        related_name="runs",
    )

    run_number = models.PositiveIntegerField()

    label = models.CharField(
        max_length=200,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SUCCESS,
    )

    request_payload = models.JSONField(
        default=dict,
    )

    result_payload = models.JSONField(
        default=dict,
    )

    metrics = models.JSONField(
        default=dict,
    )

    error_message = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )


    class Meta:
        ordering = (
            "-run_number",
        )

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "scenario",
                    "run_number",
                ),

                name=(
                    "unique_run_number_per_scenario"
                ),
            ),
        ]


    def __str__(self):
        return (
            f"{self.scenario.name}"
            f" - Run {self.run_number}"
        )
