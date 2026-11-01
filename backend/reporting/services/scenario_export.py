from django.utils import timezone

from reporting.constants import (
    RUN_REPORT_SCHEMA,
    SCENARIO_SCHEMA,
    SCHEMA_VERSION,
)


def _datetime_value(
    value,
):
    if value is None:
        return None


    return value.isoformat()


def serialize_run(
    run,
):
    return {
        "id":
            run.id,

        "run_number":
            run.run_number,

        "label":
            run.label,

        "status":
            run.status,

        "request_payload":
            run.request_payload,

        "result_payload":
            run.result_payload,

        "metrics":
            run.metrics,

        "error_message":
            run.error_message,

        "created_at":
            _datetime_value(
                run.created_at
            ),
    }


def build_scenario_export(
    scenario,
):
    runs = (
        scenario.runs
        .order_by(
            "run_number"
        )
    )


    return {
        "schema":
            SCENARIO_SCHEMA,

        "schema_version":
            SCHEMA_VERSION,

        "generated_at":
            timezone.now()
            .isoformat(),

        "scenario": {
            "id":
                scenario.id,

            "organization_id":
                scenario.organization_id,

            "organization_name":
                scenario
                .organization
                .name,

            "name":
                scenario.name,

            "simulation_type":
                scenario.simulation_type,

            "description":
                scenario.description,

            "request_payload":
                scenario.request_payload,

            "created_at":
                _datetime_value(
                    scenario.created_at
                ),

            "updated_at":
                _datetime_value(
                    scenario.updated_at
                ),
        },

        "runs": [
            serialize_run(
                run
            )

            for run
            in runs
        ],
    }


def build_run_report(
    run,
):
    scenario = (
        run.scenario
    )


    return {
        "schema":
            RUN_REPORT_SCHEMA,

        "schema_version":
            SCHEMA_VERSION,

        "generated_at":
            timezone.now()
            .isoformat(),

        "organization": {
            "id":
                scenario.organization_id,

            "name":
                scenario
                .organization
                .name,
        },

        "scenario": {
            "id":
                scenario.id,

            "name":
                scenario.name,

            "simulation_type":
                scenario.simulation_type,

            "description":
                scenario.description,
        },

        "run":
            serialize_run(
                run
            ),

        "interpretation": {
            "type":
                (
                    "modeled-simulation-"
                    "result"
                ),

            "statement":
                (
                    "This report describes "
                    "the result of a modeled "
                    "RiftTrace simulation. "
                    "It does not represent "
                    "an observed cyberattack "
                    "or a prediction of exact "
                    "attacker behavior."
                ),
        },
    }
