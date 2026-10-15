import csv
from pathlib import Path

from django.core.management.base import (
    BaseCommand,
)

from assets.models import Asset

from organizations.models import (
    Organization,
)

from security.models import (
    SecurityControl,
)

from simulations.services import (
    load_business_context,
    load_organization_graph,
    load_security_control_context,
)

from simulation_engine.prioritization import (
    rank_security_controls,
)


class Command(BaseCommand):
    help = (
        "Evaluate RiftTrace demo scenarios "
        "and export control-ranking results."
    )


    def add_arguments(self, parser):
        parser.add_argument(
            "--organization",

            default="RiftTrace Labs",
        )


        parser.add_argument(
            "--output",

            default=(
                "../docs/"
                "evaluation_results.csv"
            ),
        )


    def handle(
        self,
        *args,
        **options,
    ):
        organization = (
            Organization.objects.get(
                name=options[
                    "organization"
                ]
            )
        )


        graph_context = (
            load_organization_graph(
                organization
            )
        )


        business_context = (
            load_business_context(
                organization
            )
        )


        control_ids = list(
            SecurityControl.objects.filter(
                organization=organization
            )
            .order_by("id")
            .values_list(
                "id",
                flat=True,
            )
        )


        if not control_ids:
            raise RuntimeError(
                "No security controls exist."
            )


        control_context = (
            load_security_control_context(
                organization,

                control_ids,
            )
        )


        scenario_names = [
            "Public Web App",
            "VPN Gateway",
            "Admin Workstation",
            "CI/CD Server",
            "Internal API",
        ]


        output_path = Path(
            options[
                "output"
            ]
        )


        output_path.parent.mkdir(
            parents=True,

            exist_ok=True,
        )


        rows = []


        for asset_name in (
            scenario_names
        ):
            start_asset = (
                Asset.objects.filter(
                    organization=(
                        organization
                    ),

                    name=asset_name,
                )
                .first()
            )


            if start_asset is None:
                self.stdout.write(
                    self.style.WARNING(
                        (
                            "Skipping missing "
                            "demo asset: "
                            f"{asset_name}"
                        )
                    )
                )

                continue


            ranking = (
                rank_security_controls(
                    graph=(
                        graph_context.graph
                    ),

                    vulnerabilities=(
                        graph_context
                        .vulnerability_records
                    ),

                    business_processes=(
                        business_context
                        .process_records
                    ),

                    dependencies=(
                        business_context
                        .dependency_records
                    ),

                    controls=(
                        control_context.records
                    ),

                    start_asset_id=(
                        start_asset.id
                    ),

                    start_privilege="LOW",
                )
            )


            for item in (
                ranking.ranked_controls
            ):
                control = (
                    control_context
                    .controls_by_id[
                        item.control_id
                    ]
                )


                rows.append(
                    {
                        "scenario_start_asset":
                            asset_name,

                        "start_privilege":
                            "LOW",

                        "rank":
                            item.priority_rank,

                        "control_name":
                            control.name,

                        "control_type":
                            control
                            .control_type,

                        "has_measured_effect":
                            item
                            .has_measured_effect,

                        "critical_process_reduction":
                            item
                            .metrics
                            .critical_process_reduction,

                        "critical_asset_reduction":
                            item
                            .metrics
                            .critical_asset_reduction,

                        "essential_dependency_hit_reduction":
                            item
                            .metrics
                            .essential_dependency_hit_reduction,

                        "impacted_process_reduction":
                            item
                            .metrics
                            .impacted_process_reduction,

                        "propagated_asset_reduction":
                            item
                            .metrics
                            .propagated_asset_reduction,
                    }
                )


        fieldnames = [
            "scenario_start_asset",
            "start_privilege",
            "rank",
            "control_name",
            "control_type",
            "has_measured_effect",
            "critical_process_reduction",
            "critical_asset_reduction",
            "essential_dependency_hit_reduction",
            "impacted_process_reduction",
            "propagated_asset_reduction",
        ]


        with output_path.open(
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
                    "Evaluation written to "
                    f"{output_path}"
                )
            )
        )
