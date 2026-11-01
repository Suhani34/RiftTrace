from django.urls import path

from .views import (
    EnvironmentExportView,
    EnvironmentIngestionExportView,
    ReportingSummaryView,
    ScenarioExportView,
    ScenarioRunMetricsCsvView,
    ScenarioRunReportView,
)


urlpatterns = [
    path(
        "summary/",
        ReportingSummaryView.as_view(),
        name="reporting-summary",
    ),

    path(
        (
            "environment/"
            "<int:organization_id>/"
        ),
        EnvironmentExportView.as_view(),
        name="environment-export",
    ),

    path(
        (
            "environment/"
            "<int:organization_id>/"
            "ingestion/"
        ),
        EnvironmentIngestionExportView.as_view(),
        name=(
            "environment-ingestion-export"
        ),
    ),

    path(
        (
            "scenarios/"
            "<int:scenario_id>/"
        ),
        ScenarioExportView.as_view(),
        name="scenario-export",
    ),

    path(
        (
            "runs/"
            "<int:run_id>/"
        ),
        ScenarioRunReportView.as_view(),
        name="run-report",
    ),

    path(
        (
            "runs/"
            "<int:run_id>/"
            "metrics.csv"
        ),
        ScenarioRunMetricsCsvView.as_view(),
        name="run-metrics-csv",
    ),
]
