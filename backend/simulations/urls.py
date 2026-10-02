from django.urls import path

from .views import (
    BusinessImpactSimulationView,
    AttackPropagationView,
    ReachabilitySimulationView,
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
]
