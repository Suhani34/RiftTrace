from django.urls import path

from .views import (
    BusinessImpactSimulationView,
    AttackPropagationView,
    ReachabilitySimulationView,
    CounterfactualSimulationView,
    SecurityControlSimulationView,
    SecurityControlRankingView,
)


urlpatterns = [
    path(
        "reachability/",
        ReachabilitySimulationView.as_view(),
        name="simulation-reachability",
    ),
    path(
        "attack-propagation/",
        AttackPropagationView.as_view(),
        name="simulation-attack-propagation",
    ),
    path(
        "business-impact/",
        BusinessImpactSimulationView.as_view(),
        name="simulation-business-impact",
    ),
    path(
        "counterfactual/",
        CounterfactualSimulationView.as_view(),
        name="simulation-counterfactual",
    ),
    path(
        "security-controls/",
        SecurityControlSimulationView.as_view(),
        name=(
            "simulation-security-controls"
        ),
    ),
    path(
        "control-ranking/",
        SecurityControlRankingView.as_view(),
        name=(
            "simulation-control-ranking"
        ),
    ),
]

