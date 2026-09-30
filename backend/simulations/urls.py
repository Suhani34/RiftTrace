from django.urls import path

from .views import (
    ReachabilitySimulationView,
)


urlpatterns = [
    path(
        "reachability/",
        ReachabilitySimulationView.as_view(),
        name="simulation-reachability",
    ),
]
