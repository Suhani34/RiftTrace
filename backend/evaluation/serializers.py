from rest_framework import serializers

from scenarios.models import (
    ScenarioRun,
)

from .models import (
    EvaluationExperiment,
)

from .services import (
    build_experiment_comparison,
)


class EvaluationExperimentSerializer(
    serializers.ModelSerializer
):
    organization_name = (
        serializers.CharField(
            source="organization.name",
            read_only=True,
        )
    )

    scenario_name = (
        serializers.CharField(
            source="scenario.name",
            read_only=True,
        )
    )

    simulation_type = (
        serializers.CharField(
            source=(
                "scenario.simulation_type"
            ),
            read_only=True,
        )
    )

    baseline_run_number = (
        serializers.IntegerField(
            source=(
                "baseline_run.run_number"
            ),
            read_only=True,
        )
    )

    treatment_run_number = (
        serializers.IntegerField(
            source=(
                "treatment_run.run_number"
            ),
            read_only=True,
        )
    )

    comparison = (
        serializers.SerializerMethodField()
    )


    class Meta:
        model = EvaluationExperiment

        fields = (
            "id",
            "organization",
            "organization_name",
            "name",
            "scenario",
            "scenario_name",
            "simulation_type",
            "baseline_run",
            "baseline_run_number",
            "treatment_run",
            "treatment_run_number",
            "intervention_label",
            "notes",
            "comparison",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "organization_name",
            "scenario_name",
            "simulation_type",
            "baseline_run_number",
            "treatment_run_number",
            "comparison",
            "created_at",
            "updated_at",
        )


    def get_comparison(
        self,
        obj,
    ):
        return (
            build_experiment_comparison(
                obj
            )
        )


    def validate(
        self,
        attrs,
    ):
        instance = (
            self.instance
        )


        organization = (
            attrs.get(
                "organization"
            )
            or (
                instance.organization
                if instance
                else None
            )
        )

        scenario = (
            attrs.get(
                "scenario"
            )
            or (
                instance.scenario
                if instance
                else None
            )
        )

        baseline_run = (
            attrs.get(
                "baseline_run"
            )
            or (
                instance.baseline_run
                if instance
                else None
            )
        )

        treatment_run = (
            attrs.get(
                "treatment_run"
            )
            or (
                instance.treatment_run
                if instance
                else None
            )
        )


        if (
            organization
            and scenario
            and (
                scenario.organization_id
                != organization.id
            )
        ):
            raise serializers.ValidationError(
                {
                    "scenario":
                        (
                            "Scenario must belong "
                            "to the selected "
                            "organization."
                        )
                }
            )


        if (
            scenario
            and baseline_run
            and (
                baseline_run.scenario_id
                != scenario.id
            )
        ):
            raise serializers.ValidationError(
                {
                    "baseline_run":
                        (
                            "Baseline run must "
                            "belong to this "
                            "scenario."
                        )
                }
            )


        if (
            scenario
            and treatment_run
            and (
                treatment_run.scenario_id
                != scenario.id
            )
        ):
            raise serializers.ValidationError(
                {
                    "treatment_run":
                        (
                            "Treatment run must "
                            "belong to this "
                            "scenario."
                        )
                }
            )


        if (
            baseline_run
            and treatment_run
            and (
                baseline_run.id
                == treatment_run.id
            )
        ):
            raise serializers.ValidationError(
                {
                    "treatment_run":
                        (
                            "Baseline and "
                            "treatment runs must "
                            "be different."
                        )
                }
            )


        if (
            baseline_run
            and (
                baseline_run.status
                != ScenarioRun.Status.SUCCESS
            )
        ):
            raise serializers.ValidationError(
                {
                    "baseline_run":
                        (
                            "Baseline run must "
                            "be successful."
                        )
                }
            )


        if (
            treatment_run
            and (
                treatment_run.status
                != ScenarioRun.Status.SUCCESS
            )
        ):
            raise serializers.ValidationError(
                {
                    "treatment_run":
                        (
                            "Treatment run must "
                            "be successful."
                        )
                }
            )


        if (
            baseline_run
            and treatment_run
            and (
                baseline_run.run_number
                >= treatment_run.run_number
            )
        ):
            raise serializers.ValidationError(
                {
                    "treatment_run":
                        (
                            "Treatment run must "
                            "occur after the "
                            "baseline run."
                        )
                }
            )


        return attrs
