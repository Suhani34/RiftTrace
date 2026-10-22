from rest_framework import serializers

from .constants import COMPARABLE_METRICS
from .models import (
    SavedScenario,
    ScenarioRun,
)


class SavedScenarioSerializer(
    serializers.ModelSerializer
):
    organization_name = (
        serializers.CharField(
            source="organization.name",
            read_only=True,
        )
    )

    run_count = (
        serializers.SerializerMethodField()
    )

    latest_run_number = (
        serializers.SerializerMethodField()
    )

    latest_run_at = (
        serializers.SerializerMethodField()
    )


    class Meta:
        model = SavedScenario

        fields = (
            "id",
            "organization",
            "organization_name",
            "name",
            "simulation_type",
            "description",
            "request_payload",
            "run_count",
            "latest_run_number",
            "latest_run_at",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "organization_name",
            "run_count",
            "latest_run_number",
            "latest_run_at",
            "created_at",
            "updated_at",
        )


    def validate_request_payload(
        self,
        value,
    ):
        if not isinstance(
            value,
            dict,
        ):
            raise serializers.ValidationError(
                "request_payload must be a JSON object."
            )

        return value


    def get_run_count(
        self,
        obj,
    ):
        return obj.runs.count()


    def get_latest_run_number(
        self,
        obj,
    ):
        latest_run = (
            obj.runs
            .order_by(
                "-run_number"
            )
            .first()
        )

        if latest_run is None:
            return None

        return latest_run.run_number


    def get_latest_run_at(
        self,
        obj,
    ):
        latest_run = (
            obj.runs
            .order_by(
                "-run_number"
            )
            .first()
        )

        if latest_run is None:
            return None

        return latest_run.created_at


class ScenarioRunSerializer(
    serializers.ModelSerializer
):
    scenario_name = (
        serializers.CharField(
            source="scenario.name",
            read_only=True,
        )
    )


    class Meta:
        model = ScenarioRun

        fields = (
            "id",
            "scenario",
            "scenario_name",
            "run_number",
            "label",
            "status",
            "request_payload",
            "result_payload",
            "metrics",
            "error_message",
            "created_at",
        )

        read_only_fields = fields


class ScenarioRunCreateSerializer(
    serializers.Serializer
):
    label = serializers.CharField(
        required=False,
        allow_blank=True,
        default="",
        max_length=200,
    )

    status = serializers.ChoiceField(
        required=False,
        default=ScenarioRun.Status.SUCCESS,
        choices=ScenarioRun.Status.choices,
    )

    request_payload = (
        serializers.JSONField(
            required=False,
        )
    )

    result_payload = (
        serializers.JSONField(
            required=False,
            default=dict,
        )
    )

    metrics = serializers.JSONField(
        required=False,
        default=dict,
    )

    error_message = (
        serializers.CharField(
            required=False,
            allow_blank=True,
            default="",
        )
    )


    def validate_request_payload(
        self,
        value,
    ):
        if not isinstance(
            value,
            dict,
        ):
            raise serializers.ValidationError(
                "request_payload must be a JSON object."
            )

        return value


    def validate_metrics(
        self,
        value,
    ):
        if not isinstance(
            value,
            dict,
        ):
            raise serializers.ValidationError(
                "metrics must be a JSON object."
            )


        for (
            metric_key,
            metric_value,
        ) in value.items():
            if (
                metric_key
                not in COMPARABLE_METRICS
            ):
                raise serializers.ValidationError(
                    (
                        f"Unsupported comparable metric: "
                        f"{metric_key}"
                    )
                )


            if (
                isinstance(
                    metric_value,
                    bool,
                )
                or not isinstance(
                    metric_value,
                    (
                        int,
                        float,
                    ),
                )
            ):
                raise serializers.ValidationError(
                    (
                        f"{metric_key} must be numeric."
                    )
                )


            if metric_value < 0:
                raise serializers.ValidationError(
                    (
                        f"{metric_key} cannot be negative."
                    )
                )


        return value


    def validate(
        self,
        attrs,
    ):
        status_value = attrs.get(
            "status",
            ScenarioRun.Status.SUCCESS,
        )

        error_message = attrs.get(
            "error_message",
            "",
        )


        if (
            status_value
            == ScenarioRun.Status.FAILED
            and not error_message.strip()
        ):
            raise serializers.ValidationError(
                {
                    "error_message":
                        (
                            "A failed run must include "
                            "an error message."
                        )
                }
            )


        return attrs
