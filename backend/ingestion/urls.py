from django.urls import path

from .views import (
    IngestionApplyView,
    IngestionPreviewView,
    IngestionRunListView,
)


urlpatterns = [
    path(
        "preview/",

        IngestionPreviewView.as_view(),

        name="ingestion-preview",
    ),

    path(
        "apply/",

        IngestionApplyView.as_view(),

        name="ingestion-apply",
    ),

    path(
        "runs/",

        IngestionRunListView.as_view(),

        name="ingestion-runs",
    ),
]
