import csv
import io
import json

from django.http import (
    HttpResponse,
)

from django.shortcuts import (
    get_object_or_404,
)

from rest_framework.response import (
    Response,
)

from rest_framework.views import (
    APIView,
)

from organizations.models import (
    Organization,
)

from scenarios.models import (
    SavedScenario,
    ScenarioRun,
)

from reporting.services.environment_export import (
    build_ingestion_environment,
    build_portable_environment,
)

from reporting.services.scenario_export import (
    build_run_report,
    build_scenario_export,
)

from reporting.services.summary import (
    build_reporting_summary,
)


def json_download_response(
    payload,
    filename,
):
    response = HttpResponse(
        json.dumps(
            payload,
            indent=2,
            default=str,
        ),

        content_type=(
            "application/json"
        ),
    )


    response[
        "Content-Disposition"
    ] = (
        f'attachment; '
        f'filename="{filename}"'
    )


    return response


class ReportingSummaryView(
    APIView
):
    def get(
        self,
        request,
    ):
        organization_id = (
            request
            .query_params
            .get(
                "organization"
            )
        )


        if not organization_id:
            return Response(
                {
                    "detail":
                        (
                            "organization "
                            "is required."
                        )
                },

                status=400,
            )


        organization = (
            get_object_or_404(
                Organization,
                pk=organization_id,
            )
        )


        return Response(
            build_reporting_summary(
                organization
            )
        )


class EnvironmentExportView(
    APIView
):
    def get(
        self,
        request,
        organization_id,
    ):
        organization = (
            get_object_or_404(
                Organization,
                pk=organization_id,
            )
        )


        payload = (
            build_portable_environment(
                organization
            )
        )


        return json_download_response(
            payload,

            (
                f"rifttrace_"
                f"environment_"
                f"{organization.id}.json"
            ),
        )


class EnvironmentIngestionExportView(
    APIView
):
    def get(
        self,
        request,
        organization_id,
    ):
        organization = (
            get_object_or_404(
                Organization,
                pk=organization_id,
            )
        )


        payload = (
            build_ingestion_environment(
                organization
            )
        )


        return json_download_response(
            payload,

            (
                f"rifttrace_"
                f"ingestion_"
                f"{organization.id}.json"
            ),
        )


class ScenarioExportView(
    APIView
):
    def get(
        self,
        request,
        scenario_id,
    ):
        scenario = (
            get_object_or_404(
                SavedScenario.objects
                .select_related(
                    "organization"
                ),

                pk=scenario_id,
            )
        )


        payload = (
            build_scenario_export(
                scenario
            )
        )


        return json_download_response(
            payload,

            (
                f"rifttrace_"
                f"scenario_"
                f"{scenario.id}.json"
            ),
        )


class ScenarioRunReportView(
    APIView
):
    def get(
        self,
        request,
        run_id,
    ):
        run = (
            get_object_or_404(
                ScenarioRun.objects
                .select_related(
                    "scenario",
                    "scenario__organization",
                ),

                pk=run_id,
            )
        )


        payload = (
            build_run_report(
                run
            )
        )


        return json_download_response(
            payload,

            (
                f"rifttrace_"
                f"run_"
                f"{run.id}.json"
            ),
        )


class ScenarioRunMetricsCsvView(
    APIView
):
    def get(
        self,
        request,
        run_id,
    ):
        run = (
            get_object_or_404(
                ScenarioRun.objects
                .select_related(
                    "scenario",
                    "scenario__organization",
                ),

                pk=run_id,
            )
        )


        output = (
            io.StringIO()
        )


        writer = csv.writer(
            output
        )


        writer.writerow(
            [
                "schema_version",
                "scenario_id",
                "scenario_name",
                "simulation_type",
                "run_id",
                "run_number",
                "status",
                "metric",
                "value",
            ]
        )


        metrics = (
            run.metrics
            if isinstance(
                run.metrics,
                dict,
            )
            else {}
        )


        for metric_name in sorted(
            metrics
        ):
            metric_value = (
                metrics[
                    metric_name
                ]
            )


            writer.writerow(
                [
                    "1.0",
                    run.scenario_id,
                    run.scenario.name,
                    run.scenario.simulation_type,
                    run.id,
                    run.run_number,
                    run.status,
                    metric_name,
                    metric_value,
                ]
            )


        response = HttpResponse(
            output.getvalue(),

            content_type=(
                "text/csv"
            ),
        )


        response[
            "Content-Disposition"
        ] = (
            f'attachment; '
            f'filename="rifttrace_'
            f'run_{run.id}_metrics.csv"'
        )


        return response
