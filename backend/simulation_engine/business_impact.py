from collections import defaultdict
from dataclasses import dataclass

from .business_records import (
    BusinessDependencyRecord,
    BusinessProcessRecord,
)


DEPENDENCY_RANK = {
    "SUPPORTING": 1,
    "IMPORTANT": 2,
    "ESSENTIAL": 3,
}


PROCESS_CRITICALITY_RANK = {
    "LOW": 1,
    "MEDIUM": 2,
    "HIGH": 3,
    "CRITICAL": 4,
}


@dataclass(
    frozen=True,
    slots=True,
)
class ImpactedBusinessProcess:
    business_process_id: int

    criticality: str

    strongest_dependency_level: str

    affected_asset_ids: tuple[
        int,
        ...,
    ]

    affected_dependency_ids: tuple[
        int,
        ...,
    ]


@dataclass(
    frozen=True,
    slots=True,
)
class BusinessImpactResult:
    impacted_processes: tuple[
        ImpactedBusinessProcess,
        ...,
    ]

    impacted_process_count: int

    critical_process_count: int

    essential_dependency_hit_count: int


def analyze_business_impact(
    business_processes: tuple[
        BusinessProcessRecord,
        ...,
    ],

    dependencies: tuple[
        BusinessDependencyRecord,
        ...,
    ],

    affected_asset_ids: set[int],
) -> BusinessImpactResult:
    processes_by_id = {
        process.id: process

        for process
        in business_processes
    }


    dependencies_by_process: dict[
        int,
        list[BusinessDependencyRecord],
    ] = defaultdict(list)


    for dependency in dependencies:
        dependencies_by_process[
            dependency
            .business_process_id
        ].append(
            dependency
        )


    impacted = []


    for (
        business_process_id,
        process_dependencies,
    ) in dependencies_by_process.items():
        process = processes_by_id.get(
            business_process_id
        )

        if process is None:
            continue


        affected_dependencies = [
            dependency

            for dependency
            in process_dependencies

            if (
                dependency.asset_id
                in affected_asset_ids
            )
        ]


        if not affected_dependencies:
            continue


        strongest = max(
            affected_dependencies,

            key=lambda dependency: (
                DEPENDENCY_RANK[
                    dependency
                    .dependency_level
                ]
            ),
        )


        affected_assets = tuple(
            sorted(
                {
                    dependency.asset_id

                    for dependency
                    in affected_dependencies
                }
            )
        )


        affected_dependency_ids = tuple(
            sorted(
                dependency.id

                for dependency
                in affected_dependencies
            )
        )


        impacted.append(
            ImpactedBusinessProcess(
                business_process_id=(
                    process.id
                ),

                criticality=(
                    process.criticality
                ),

                strongest_dependency_level=(
                    strongest
                    .dependency_level
                ),

                affected_asset_ids=(
                    affected_assets
                ),

                affected_dependency_ids=(
                    affected_dependency_ids
                ),
            )
        )


    impacted.sort(
        key=lambda result: (
            -PROCESS_CRITICALITY_RANK[
                result.criticality
            ],

            -DEPENDENCY_RANK[
                result
                .strongest_dependency_level
            ],

            result.business_process_id,
        )
    )


    critical_process_count = sum(
        1

        for process
        in impacted

        if (
            process.criticality
            == "CRITICAL"
        )
    )


    impacted_dependency_ids = {
        dependency_id

        for process
        in impacted

        for dependency_id
        in process.affected_dependency_ids
    }


    dependencies_by_id = {
        dependency.id: dependency

        for dependency
        in dependencies
    }


    essential_dependency_hit_count = sum(
        1

        for dependency_id
        in impacted_dependency_ids

        if (
            dependencies_by_id[
                dependency_id
            ].dependency_level
            == "ESSENTIAL"
        )
    )


    return BusinessImpactResult(
        impacted_processes=tuple(
            impacted
        ),

        impacted_process_count=len(
            impacted
        ),

        critical_process_count=(
            critical_process_count
        ),

        essential_dependency_hit_count=(
            essential_dependency_hit_count
        ),
    )
