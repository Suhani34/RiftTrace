from dataclasses import dataclass

import networkx as nx

from .business_records import (
    BusinessDependencyRecord,
    BusinessProcessRecord,
)

from .control_records import (
    SecurityControlRecord,
)

from .counterfactual import (
    CounterfactualComparison,
)

from .records import (
    VulnerabilityRecord,
)

from .security_controls import (
    analyze_security_controls,
)


@dataclass(
    frozen=True,
    slots=True,
)
class ControlReductionMetrics:
    critical_process_reduction: int

    critical_asset_reduction: int

    essential_dependency_hit_reduction: int

    impacted_process_reduction: int

    propagated_asset_reduction: int


@dataclass(
    frozen=True,
    slots=True,
)
class RankedSecurityControl:
    control_id: int

    priority_rank: int

    metrics: ControlReductionMetrics

    comparison: CounterfactualComparison

    has_measured_effect: bool


@dataclass(
    frozen=True,
    slots=True,
)
class SecurityControlRankingResult:
    ranked_controls: tuple[
        RankedSecurityControl,
        ...,
    ]


def _metrics_from_comparison(
    comparison: CounterfactualComparison,
) -> ControlReductionMetrics:
    return ControlReductionMetrics(
        critical_process_reduction=(
            comparison
            .critical_process_reduction
        ),

        critical_asset_reduction=(
            comparison
            .critical_asset_reduction
        ),

        essential_dependency_hit_reduction=(
            comparison
            .essential_dependency_hit_reduction
        ),

        impacted_process_reduction=(
            comparison
            .impacted_process_reduction
        ),

        propagated_asset_reduction=(
            comparison
            .propagated_asset_reduction
        ),
    )


def _priority_signature(
    metrics: ControlReductionMetrics,
) -> tuple[
    int,
    int,
    int,
    int,
    int,
]:
    return (
        metrics
        .critical_process_reduction,

        metrics
        .critical_asset_reduction,

        metrics
        .essential_dependency_hit_reduction,

        metrics
        .impacted_process_reduction,

        metrics
        .propagated_asset_reduction,
    )


def _has_measured_effect(
    metrics: ControlReductionMetrics,
) -> bool:
    return any(
        value > 0

        for value
        in _priority_signature(
            metrics
        )
    )


def rank_security_controls(
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

    controls: tuple[
        SecurityControlRecord,
        ...,
    ],

    start_asset_id: int,

    start_privilege: str,
) -> SecurityControlRankingResult:
    if not controls:
        raise ValueError(
            "At least one security "
            "control is required."
        )


    evaluations = []


    for control in controls:
        simulation = (
            analyze_security_controls(
                graph=graph,

                vulnerabilities=(
                    vulnerabilities
                ),

                business_processes=(
                    business_processes
                ),

                dependencies=(
                    dependencies
                ),

                controls=(
                    control,
                ),

                start_asset_id=(
                    start_asset_id
                ),

                start_privilege=(
                    start_privilege
                ),
            )
        )


        comparison = (
            simulation.comparison
        )


        metrics = (
            _metrics_from_comparison(
                comparison
            )
        )


        evaluations.append(
            (
                control.id,
                metrics,
                comparison,
            )
        )


    evaluations.sort(
        key=lambda item: (
            -item[
                1
            ].critical_process_reduction,

            -item[
                1
            ].critical_asset_reduction,

            -item[
                1
            ].essential_dependency_hit_reduction,

            -item[
                1
            ].impacted_process_reduction,

            -item[
                1
            ].propagated_asset_reduction,

            item[0],
        )
    )


    ranked_controls = []

    previous_signature = None

    current_rank = 0


    for (
        control_id,
        metrics,
        comparison,
    ) in evaluations:
        signature = (
            _priority_signature(
                metrics
            )
        )


        if (
            signature
            != previous_signature
        ):
            current_rank += 1

            previous_signature = (
                signature
            )


        ranked_controls.append(
            RankedSecurityControl(
                control_id=(
                    control_id
                ),

                priority_rank=(
                    current_rank
                ),

                metrics=metrics,

                comparison=(
                    comparison
                ),

                has_measured_effect=(
                    _has_measured_effect(
                        metrics
                    )
                ),
            )
        )


    return SecurityControlRankingResult(
        ranked_controls=tuple(
            ranked_controls
        )
    )
