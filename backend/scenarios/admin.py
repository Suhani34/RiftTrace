from django.contrib import admin

from .models import (
    SavedScenario,
    ScenarioRun,
)


@admin.register(SavedScenario)
class SavedScenarioAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "organization",
        "simulation_type",
        "updated_at",
    )

    list_filter = (
        "simulation_type",
        "organization",
    )

    search_fields = (
        "name",
        "description",
    )


@admin.register(ScenarioRun)
class ScenarioRunAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "scenario",
        "run_number",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "scenario__simulation_type",
    )

    search_fields = (
        "scenario__name",
        "label",
    )
