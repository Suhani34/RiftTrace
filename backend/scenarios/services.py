from django.db import transaction
from django.db.models import Max

from .constants import COMPARABLE_METRICS
from .models import (
    SavedScenario,
    ScenarioRun,
)


def _is_number(
    value,
):
    return (
        isinstance(
            value,
            (
                int,
                float,
            ),
        )
        and not isinstance(
            value,
            bool,
        )
    )


@transaction.atomic
def create_scenario_run(
    *,
    scenario,
    request_payload,
    result_payload,
    metrics,
    status,
    label="",
    error_message="",
):
    locked_scenario = (
        SavedScenario.objects
        .select_for_update()
        .get(
            pk=scenario.pk
        )
    )


    latest_number = (
        locked_scenario
        .runs
        .aggregate(
            maximum=Max(
                "run_number"
            )
        )
        .get(
            "maximum"
        )
        or 0
    )


    return ScenarioRun.objects.create(
        scenario=locked_scenario,

        run_number=(
            latest_number + 1
        ),

        label=label,

        status=status,

        request_payload=(
            request_payload
        ),

        result_payload=(
            result_payload
        ),

        metrics=metrics,

        error_message=(
            error_message
        ),
    )


def compare_scenario_runs(
    before_run,
    after_run,
):
    if (
        before_run.scenario_id
        != after_run.scenario_id
    ):
        raise ValueError(
            "Runs must belong to the same scenario."
        )


    if (
        before_run.status
        != ScenarioRun.Status.SUCCESS
    ):
        raise ValueError(
            "The before run must be successful."
        )


    if (
        after_run.status
        != ScenarioRun.Status.SUCCESS
    ):
        raise ValueError(
            "The after run must be successful."
        )


    before_metrics = (
        before_run.metrics
        if isinstance(
            before_run.metrics,
            dict,
        )
        else {}
    )

    after_metrics = (
        after_run.metrics
        if isinstance(
            after_run.metrics,
            dict,
        )
        else {}
    )


    metric_differences = []


    for metric_key, metric_label in (
        COMPARABLE_METRICS.items()
    ):
        before_value = (
            before_metrics.get(
                metric_key
            )
        )

        after_value = (
            after_metrics.get(
                metric_key
            )
        )


        if not (
            _is_number(
                before_value
            )
            and _is_number(
                after_value
            )
        ):
            continue


        delta = (
            after_value
            - before_value
        )

        reduction = (
            before_value
            - after_value
        )


        if reduction > 0:
            interpretation = (
                "IMPROVED"
            )

        elif reduction < 0:
            interpretation = (
                "WORSENED"
            )

        else:
            interpretation = (
                "UNCHANGED"
            )


        metric_differences.append(
            {
                "metric":
                    metric_key,

                "label":
                    metric_label,

                "before":
                    before_value,

                "after":
                    after_value,

                "delta":
                    delta,

                "reduction":
                    reduction,

                "interpretation":
                    interpretation,
            }
        )


    return metric_differences
