from django.contrib import admin

from .models import (
    EvaluationExperiment,
)


@admin.register(EvaluationExperiment)
class EvaluationExperimentAdmin(
    admin.ModelAdmin
):
    list_display = (
        "id",
        "name",
        "organization",
        "scenario",
        "baseline_run",
        "treatment_run",
        "created_at",
    )

    list_filter = (
        "organization",
        "scenario__simulation_type",
    )

    search_fields = (
        "name",
        "intervention_label",
        "notes",
    )
