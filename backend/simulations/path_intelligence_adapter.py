from collections import defaultdict

from business.models import (
    BusinessProcess,
    BusinessProcessDependency,
)

from simulation_engine.attack_propagation import (
    analyze_attack_propagation,
)

from simulation_engine.path_records import (
    AttackTransition,
    PathTargetMetadata,
)

from .services import (
    load_organization_graph,
)


def load_path_intelligence_context(
    *,
    organization,
    start_asset,
    start_privilege,
):
    """
    Build the input required by the pure
    Phase 21 path-intelligence engine.

    Important:
    This function does NOT treat every
    Relationship as an attack path edge.

    It first runs the existing Phase 8
    security-aware propagation engine and
    only converts relationships that Phase 8
    successfully traversed.
    """

    context = (
        load_organization_graph(
            organization
        )
    )


    propagation_result = (
        analyze_attack_propagation(
            graph=context.graph,

            vulnerabilities=(
                context
                .vulnerability_records
            ),

            start_asset_id=(
                start_asset.id
            ),

            start_privilege=(
                start_privilege
            ),
        )
    )


    # -------------------------------------------------
    # Effective privilege of every propagated asset
    # -------------------------------------------------

    privilege_by_asset = {
        start_asset.id:
            propagation_result
            .start_privilege
    }


    for propagated in (
        propagation_result
        .propagated_assets
    ):
        privilege_by_asset[
            propagated.asset_id
        ] = (
            propagated.privilege
        )


    # -------------------------------------------------
    # Map the relationship that actually led to each
    # selected propagated-asset path to its
    # vulnerability.
    #
    # Phase 8 stores one selected path per reached
    # asset. For other successful traversed edges we
    # still know the edge was security-valid, but we
    # avoid inventing a vulnerability attribution.
    # -------------------------------------------------

    vulnerability_by_relationship = {}


    for propagated in (
        propagation_result
        .propagated_assets
    ):
        if not (
            propagated
            .path_relationship_ids
        ):
            continue


        relationship_id = (
            propagated
            .path_relationship_ids[
                -1
            ]
        )


        vulnerability_by_relationship[
            relationship_id
        ] = (
            propagated
            .via_vulnerability_id
        )


    # -------------------------------------------------
    # Convert only Phase 8 successful relationships
    # into Phase 21 transitions.
    # -------------------------------------------------

    transitions = []


    for relationship_id in (
        propagation_result
        .traversed_relationship_ids
    ):
        relationship = (
            context
            .relationships_by_id
            .get(
                relationship_id
            )
        )


        if relationship is None:
            continue


        source_asset = (
            context
            .assets_by_id[
                relationship.source_id
            ]
        )


        target_asset = (
            context
            .assets_by_id[
                relationship.target_id
            ]
        )


        vulnerability_id = (
            vulnerability_by_relationship
            .get(
                relationship_id
            )
        )


        vulnerability = None


        if (
            vulnerability_id
            is not None
        ):
            vulnerability = (
                context
                .vulnerabilities_by_id
                .get(
                    vulnerability_id
                )
            )


        transitions.append(
            AttackTransition(
                relationship_id=(
                    relationship.id
                ),

                source_asset_id=(
                    source_asset.id
                ),

                source_asset_name=(
                    source_asset.name
                ),

                source_privilege=(
                    privilege_by_asset
                    .get(
                        source_asset.id,
                        "LOW",
                    )
                ),

                target_asset_id=(
                    target_asset.id
                ),

                target_asset_name=(
                    target_asset.name
                ),

                target_privilege=(
                    privilege_by_asset
                    .get(
                        target_asset.id,
                        "LOW",
                    )
                ),

                mechanism=(
                    "VULNERABILITY_EXPLOIT"
                ),

                vulnerability_id=(
                    vulnerability.id

                    if vulnerability
                    else None
                ),

                vulnerability_title=(
                    vulnerability.title

                    if vulnerability
                    else None
                ),
            )
        )


    # -------------------------------------------------
    # Load business-process information for targets
    # -------------------------------------------------

    processes_by_asset = (
        defaultdict(
            list
        )
    )


    critical_processes_by_asset = (
        defaultdict(
            list
        )
    )


    dependencies = (
        BusinessProcessDependency
        .objects
        .filter(
            asset__organization=(
                organization
            ),

            business_process__organization=(
                organization
            ),
        )
        .select_related(
            "asset",
            "business_process",
        )
    )


    for dependency in dependencies:
        process = (
            dependency
            .business_process
        )


        processes_by_asset[
            dependency.asset_id
        ].append(
            process.name
        )


        if (
            process.criticality
            == (
                BusinessProcess
                .Criticality
                .CRITICAL
            )
        ):
            critical_processes_by_asset[
                dependency.asset_id
            ].append(
                process.name
            )


    # -------------------------------------------------
    # Build metadata for every asset.
    #
    # The pure path engine then decides which assets
    # should automatically become important targets.
    # -------------------------------------------------

    target_metadata = {}


    for (
        asset_id,
        asset,
    ) in (
        context
        .assets_by_id
        .items()
    ):
        business_process_names = (
            tuple(
                sorted(
                    set(
                        processes_by_asset[
                            asset_id
                        ]
                    )
                )
            )
        )


        critical_process_names = (
            tuple(
                sorted(
                    set(
                        critical_processes_by_asset[
                            asset_id
                        ]
                    )
                )
            )
        )


        target_metadata[
            asset_id
        ] = (
            PathTargetMetadata(
                asset_id=(
                    asset.id
                ),

                asset_name=(
                    asset.name
                ),

                criticality=(
                    asset.criticality
                ),

                business_processes=(
                    business_process_names
                ),

                critical_business_processes=(
                    critical_process_names
                ),
            )
        )


    effective_start_privilege = (
        propagation_result
        .start_privilege
    )


    return (
        tuple(
            transitions
        ),

        target_metadata,

        effective_start_privilege,
    )
