from dataclasses import dataclass

import networkx as nx

from .attack_propagation import (
    AttackPropagationResult,
    analyze_attack_propagation,
)

from .business_impact import (
    BusinessImpactResult,
    analyze_business_impact,
)

from .business_records import (
    BusinessDependencyRecord,
    BusinessProcessRecord,
)

from .records import (
    VulnerabilityRecord,
)


@dataclass(
    frozen=True,
    slots=True,
)
class CounterfactualRun:
    propagation: AttackPropagationResult

    business_impact: BusinessImpactResult

    affected_asset_ids: tuple[
        int,
        ...,
    ]


@dataclass(
    frozen=True,
    slots=True,
)
class CounterfactualComparison:
    baseline: CounterfactualRun

    counterfactual: CounterfactualRun

    prevented_propagated_asset_ids: tuple[
        int,
        ...,
    ]

    prevented_critical_asset_ids: tuple[
        int,
        ...,
    ]

    avoided_business_process_ids: tuple[
        int,
        ...,
    ]

    prevented_traversed_relationship_ids: tuple[
        int,
        ...,
    ]

    prevented_exploited_vulnerability_ids: tuple[
        int,
        ...,
    ]

    propagated_asset_reduction: int

    critical_asset_reduction: int

    impacted_process_reduction: int

    critical_process_reduction: int

    essential_dependency_hit_reduction: int


def _create_counterfactual_graph(
    graph: nx.MultiDiGraph,

    disabled_relationship_ids: set[
        int
    ],

    force_authentication_relationship_ids: set[
        int
    ],

    force_mfa_relationship_ids: set[
        int
    ],

    high_privilege_relationship_ids: set[
        int
    ],
) -> nx.MultiDiGraph:
    counterfactual_graph = (
        graph.copy()
    )


    for (
        source_id,
        target_id,
        edge_key,
        edge_data,
    ) in list(
        counterfactual_graph.edges(
            keys=True,
            data=True,
        )
    ):
        relationship_id = int(
            edge_data.get(
                "relationship_id",
                edge_key,
            )
        )


        if (
            relationship_id
            in disabled_relationship_ids
        ):
            counterfactual_graph.remove_edge(
                source_id,
                target_id,

                key=edge_key,
            )

            continue


        if (
            relationship_id
            in (
                force_authentication_relationship_ids
            )
        ):
            edge_data[
                "requires_authentication"
            ] = True


        if (
            relationship_id
            in force_mfa_relationship_ids
        ):
            edge_data[
                "requires_authentication"
            ] = True

            edge_data[
                "requires_mfa"
            ] = True


        if (
            relationship_id
            in high_privilege_relationship_ids
        ):
            edge_data[
                "required_source_privilege"
            ] = "HIGH"


    return counterfactual_graph

def _create_counterfactual_vulnerabilities(
    vulnerabilities: tuple[
        VulnerabilityRecord,
        ...,
    ],

    disabled_vulnerability_ids: set[
        int
    ],
) -> tuple[
    VulnerabilityRecord,
    ...,
]:
    return tuple(
        vulnerability

        for vulnerability
        in vulnerabilities

        if (
            vulnerability.id
            not in disabled_vulnerability_ids
        )
    )


def _run_scenario(
    graph: nx.MultiDiGraph,

    vulnerabilities: tuple[
        VulnerabilityRecord,
        ...,
    ],

    business_processes: tuple[
        BusinessProcessRecord,
        ...,
    ],

    dependencies: tuple[
        BusinessDependencyRecord,
        ...,
    ],

    start_asset_id: int,

    start_privilege: str,
) -> CounterfactualRun:
    propagation = (
        analyze_attack_propagation(
            graph=graph,

            vulnerabilities=(
                vulnerabilities
            ),

            start_asset_id=(
                start_asset_id
            ),

            start_privilege=(
                start_privilege
            ),
        )
    )


    affected_asset_ids = {
        start_asset_id,

        *(
            propagated.asset_id

            for propagated
            in propagation.propagated_assets
        ),
    }


    business_impact = (
        analyze_business_impact(
            business_processes=(
                business_processes
            ),

            dependencies=dependencies,

            affected_asset_ids=(
                affected_asset_ids
            ),
        )
    )


    return CounterfactualRun(
        propagation=propagation,

        business_impact=business_impact,

        affected_asset_ids=tuple(
            sorted(
                affected_asset_ids
            )
        ),
    )


def analyze_counterfactual(
    graph: nx.MultiDiGraph,

    vulnerabilities: tuple[
        VulnerabilityRecord,
        ...,
    ],

    business_processes: tuple[
        BusinessProcessRecord,
        ...,
    ],

    dependencies: tuple[
        BusinessDependencyRecord,
        ...,
    ],

    start_asset_id: int,

    start_privilege: str,

    disabled_relationship_ids: tuple[
        int,
        ...,
    ] = (),

    disabled_vulnerability_ids: tuple[
        int,
        ...,
    ] = (),

    force_authentication_relationship_ids: tuple[
        int,
        ...,
    ] = (),

    force_mfa_relationship_ids: tuple[
        int,
        ...,
    ] = (),

    high_privilege_relationship_ids: tuple[
        int,
        ...,
    ] = (),
) -> CounterfactualComparison:
    disabled_relationship_set = set(
        disabled_relationship_ids
    )

    disabled_vulnerability_set = set(
        disabled_vulnerability_ids
    )

    force_authentication_set = set(
        force_authentication_relationship_ids
    )

    force_mfa_set = set(
        force_mfa_relationship_ids
    )

    high_privilege_set = set(
        high_privilege_relationship_ids
    )

    baseline = _run_scenario(
        graph=graph,

        vulnerabilities=(
            vulnerabilities
        ),

        business_processes=(
            business_processes
        ),

        dependencies=dependencies,

        start_asset_id=(
            start_asset_id
        ),

        start_privilege=(
            start_privilege
        ),
    )

    counterfactual_graph = (
        _create_counterfactual_graph(
            graph=graph,

            disabled_relationship_ids=(
                disabled_relationship_set
            ),

            force_authentication_relationship_ids=(
                force_authentication_set
            ),

            force_mfa_relationship_ids=(
                force_mfa_set
            ),

            high_privilege_relationship_ids=(
                high_privilege_set
            ),
        )
    )

    counterfactual_vulnerabilities = (
        _create_counterfactual_vulnerabilities(
            vulnerabilities=(
                vulnerabilities
            ),

            disabled_vulnerability_ids=(
                disabled_vulnerability_set
            ),
        )
    )


    counterfactual = _run_scenario(
        graph=(
            counterfactual_graph
        ),

        vulnerabilities=(
            counterfactual_vulnerabilities
        ),

        business_processes=(
            business_processes
        ),

        dependencies=dependencies,

        start_asset_id=(
            start_asset_id
        ),

        start_privilege=(
            start_privilege
        ),
    )


    baseline_propagated = {
        asset.asset_id

        for asset
        in baseline
        .propagation
        .propagated_assets
    }


    counterfactual_propagated = {
        asset.asset_id

        for asset
        in counterfactual
        .propagation
        .propagated_assets
    }


    prevented_propagated_asset_ids = (
        baseline_propagated
        - counterfactual_propagated
    )


    prevented_critical_asset_ids = {
        asset_id

        for asset_id
        in prevented_propagated_asset_ids

        if (
            graph.nodes[
                asset_id
            ].get("criticality")
            == "CRITICAL"
        )
    }


    baseline_business_process_ids = {
        process.business_process_id

        for process
        in baseline
        .business_impact
        .impacted_processes
    }


    counterfactual_business_process_ids = {
        process.business_process_id

        for process
        in counterfactual
        .business_impact
        .impacted_processes
    }


    avoided_business_process_ids = (
        baseline_business_process_ids
        - counterfactual_business_process_ids
    )


    baseline_relationship_ids = set(
        baseline
        .propagation
        .traversed_relationship_ids
    )


    counterfactual_relationship_ids = set(
        counterfactual
        .propagation
        .traversed_relationship_ids
    )


    prevented_relationship_ids = (
        baseline_relationship_ids
        - counterfactual_relationship_ids
    )


    baseline_vulnerability_ids = set(
        baseline
        .propagation
        .exploited_vulnerability_ids
    )


    counterfactual_vulnerability_ids = set(
        counterfactual
        .propagation
        .exploited_vulnerability_ids
    )


    prevented_vulnerability_ids = (
        baseline_vulnerability_ids
        - counterfactual_vulnerability_ids
    )


    return CounterfactualComparison(
        baseline=baseline,

        counterfactual=(
            counterfactual
        ),

        prevented_propagated_asset_ids=(
            tuple(
                sorted(
                    prevented_propagated_asset_ids
                )
            )
        ),

        prevented_critical_asset_ids=(
            tuple(
                sorted(
                    prevented_critical_asset_ids
                )
            )
        ),

        avoided_business_process_ids=(
            tuple(
                sorted(
                    avoided_business_process_ids
                )
            )
        ),

        prevented_traversed_relationship_ids=(
            tuple(
                sorted(
                    prevented_relationship_ids
                )
            )
        ),

        prevented_exploited_vulnerability_ids=(
            tuple(
                sorted(
                    prevented_vulnerability_ids
                )
            )
        ),

        propagated_asset_reduction=(
    	    len(
                baseline_propagated
            )
            -
            len(
                counterfactual_propagated
            )
        ),

        critical_asset_reduction=(
            len(
                prevented_critical_asset_ids
            )
        ),

        impacted_process_reduction=(
            baseline
            .business_impact
            .impacted_process_count

            -

            counterfactual
            .business_impact
            .impacted_process_count
        ),

        critical_process_reduction=(
            baseline
            .business_impact
            .critical_process_count

            -

            counterfactual
            .business_impact
            .critical_process_count
        ),

        essential_dependency_hit_reduction=(
            baseline
            .business_impact
            .essential_dependency_hit_count

            -

            counterfactual
            .business_impact
            .essential_dependency_hit_count
        ),
    )
