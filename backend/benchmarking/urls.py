from django.urls import path

from .views import (
    BenchmarkResultListView,
)


urlpatterns = [
    path(
        "results/",
        BenchmarkResultListView.as_view(),
        name="benchmark-results",
    ),
]
