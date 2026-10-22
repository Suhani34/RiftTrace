from django.urls import path

from .views import (
    ScenarioCompareView,
    ScenarioDetailView,
    ScenarioListCreateView,
    ScenarioRunListCreateView,
)


urlpatterns = [
    path(
        "",
        ScenarioListCreateView.as_view(),
        name="scenario-list-create",
    ),

    path(
        "<int:pk>/",
        ScenarioDetailView.as_view(),
        name="scenario-detail",
    ),

    path(
        "<int:scenario_id>/runs/",
        ScenarioRunListCreateView.as_view(),
        name="scenario-runs",
    ),

    path(
        "<int:scenario_id>/compare/",
        ScenarioCompareView.as_view(),
        name="scenario-compare",
    ),
]
