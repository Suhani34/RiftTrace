import csv

from django.core.management.base import (
    BaseCommand,
)

from evaluation.models import (
    EvaluationExperiment,
)

from evaluation.services import (
    build_evaluation_rows,
)


class Command(BaseCommand):
    help = (
        "Export RiftTrace evaluation "
        "experiments to CSV."
    )


    def add_arguments(
        self,
        parser,
    ):
        parser.add_argument(
            "--organization",
            type=int,
            required=False,
        )

        parser.add_argument(
            "--output",
            type=str,
            default=(
                "rifttrace_evaluation.csv"
            ),
        )


    def handle(
        self,
        *args,
        **options,
    ):
        queryset = (
            EvaluationExperiment.objects
            .select_related(
                "organization",
                "scenario",
                "baseline_run",
                "treatment_run",
            )
        )


        organization_id = (
            options[
                "organization"
            ]
        )


        if organization_id:
            queryset = queryset.filter(
                organization_id=(
                    organization_id
                )
            )


        rows = (
            build_evaluation_rows(
                queryset
            )
        )


        output_path = (
            options[
                "output"
            ]
        )


        fieldnames = [
            "experiment_id",
            "experiment_name",
            "organization",
            "scenario",
            "simulation_type",
            "intervention",
            "baseline_run",
            "treatment_run",
            "metric",
            "metric_label",
            "before",
            "after",
            "reduction",
            "interpretation",
        ]


        with open(
            output_path,
            "w",
            newline="",
            encoding="utf-8",
        ) as csv_file:
            writer = csv.DictWriter(
                csv_file,
                fieldnames=fieldnames,
            )

            writer.writeheader()

            writer.writerows(
                rows
            )


        self.stdout.write(
            self.style.SUCCESS(
                (
                    f"Exported "
                    f"{len(rows)} rows "
                    f"to {output_path}"
                )
            )
        )
