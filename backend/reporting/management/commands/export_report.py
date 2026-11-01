import json

from pathlib import Path

from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from organizations.models import (
    Organization,
)

from scenarios.models import (
    SavedScenario,
    ScenarioRun,
)

from reporting.services.environment_export import (
    build_ingestion_environment,
    build_portable_environment,
)

from reporting.services.scenario_export import (
    build_run_report,
    build_scenario_export,
)


class Command(BaseCommand):
    help = (
        "Export RiftTrace data in "
        "machine-readable JSON format."
    )


    def add_arguments(
        self,
        parser,
    ):
        parser.add_argument(
            "--type",

            choices=(
                "environment",
                "ingestion",
                "scenario",
                "run",
            ),

            required=True,
        )


        parser.add_argument(
            "--id",
            type=int,
            required=True,
        )


        parser.add_argument(
            "--output",
            required=True,
        )


    def handle(
        self,
        *args,
        **options,
    ):
        export_type = (
            options[
                "type"
            ]
        )

        object_id = (
            options[
                "id"
            ]
        )

        output_path = Path(
            options[
                "output"
            ]
        )


        if (
            export_type
            == "environment"
        ):
            try:
                organization = (
                    Organization.objects
                    .get(
                        pk=object_id
                    )
                )

            except Organization.DoesNotExist as exc:
                raise CommandError(
                    "Organization not found."
                ) from exc


            payload = (
                build_portable_environment(
                    organization
                )
            )


        elif (
            export_type
            == "ingestion"
        ):
            try:
                organization = (
                    Organization.objects
                    .get(
                        pk=object_id
                    )
                )

            except Organization.DoesNotExist as exc:
                raise CommandError(
                    "Organization not found."
                ) from exc


            payload = (
                build_ingestion_environment(
                    organization
                )
            )


        elif (
            export_type
            == "scenario"
        ):
            try:
                scenario = (
                    SavedScenario.objects
                    .select_related(
                        "organization"
                    )
                    .get(
                        pk=object_id
                    )
                )

            except SavedScenario.DoesNotExist as exc:
                raise CommandError(
                    "Scenario not found."
                ) from exc


            payload = (
                build_scenario_export(
                    scenario
                )
            )


        else:
            try:
                run = (
                    ScenarioRun.objects
                    .select_related(
                        "scenario",
                        "scenario__organization",
                    )
                    .get(
                        pk=object_id
                    )
                )

            except ScenarioRun.DoesNotExist as exc:
                raise CommandError(
                    "Scenario run not found."
                ) from exc


            payload = (
                build_run_report(
                    run
                )
            )


        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )


        output_path.write_text(
            json.dumps(
                payload,
                indent=2,
                default=str,
            ),

            encoding="utf-8",
        )


        self.stdout.write(
            self.style.SUCCESS(
                (
                    f"Exported "
                    f"{export_type} "
                    f"{object_id} to "
                    f"{output_path}"
                )
            )
        )
