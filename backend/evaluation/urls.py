from django.urls import path

from .views import (
    EvaluationCsvExportView,
    EvaluationExperimentDetailView,
    EvaluationExperimentListCreateView,
    EvaluationSummaryView,
)


urlpatterns = [
    path(
        "experiments/",
        EvaluationExperimentListCreateView.as_view(),
        name="evaluation-experiment-list",
    ),

    path(
        "experiments/<int:pk>/",
        EvaluationExperimentDetailView.as_view(),
        name="evaluation-experiment-detail",
    ),

    path(
        "summary/",
        EvaluationSummaryView.as_view(),
        name="evaluation-summary",
    ),

    path(
        "export.csv",
        EvaluationCsvExportView.as_view(),
        name="evaluation-export",
    ),
]
