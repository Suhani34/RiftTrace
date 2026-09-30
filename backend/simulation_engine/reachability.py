from dataclasses import dataclass

import networkx as nx


@dataclass(
    frozen=True,
    slots=True,
)
class ReachableAssetPath:
    asset_id: int

    hop_count: int

    path_asset_ids: tuple[
        int,
        ...,
    ]


@dataclass(
    frozen=True,
    slots=True,
)
class ReachabilityResult:
    start_asset_id: int

    reachable_asset_ids: tuple[
        int,
        ...,
    ]

    reachable_relationship_ids: tuple[
        int,
        ...,
    ]

    paths: tuple[
        ReachableAssetPath,
        ...,
    ]

    max_hops: int


def analyze_reachability(
    graph: nx.MultiDiGraph,
    start_asset_id: int,
) -> ReachabilityResult:
    if start_asset_id not in graph:
        raise ValueError(
            "The start asset does not exist "
            "in the graph."
        )


    reachable_asset_ids = (
        nx.descendants(
            graph,
            start_asset_id,
        )
    )


    shortest_paths = (
        nx.single_source_shortest_path(
            graph,
            start_asset_id,
        )
    )


    path_results = []


    for asset_id, path in (
        shortest_paths.items()
    ):
        if asset_id == start_asset_id:
            continue


        path_results.append(
            ReachableAssetPath(
                asset_id=asset_id,

                hop_count=(
                    len(path) - 1
                ),

                path_asset_ids=tuple(
                    path
                ),
            )
        )


    path_results.sort(
        key=lambda result: (
            result.hop_count,
            result.asset_id,
        )
    )


    ordered_reachable_asset_ids = (
        tuple(
            result.asset_id
            for result in path_results
        )
    )


    reachable_region = (
        set(reachable_asset_ids)
        | {start_asset_id}
    )


    reachable_relationship_ids = []


    for (
        source_id,
        target_id,
        edge_key,
        edge_data,
    ) in graph.edges(
        keys=True,
        data=True,
    ):
        if (
            source_id in reachable_region
            and target_id
            in reachable_region
        ):
            relationship_id = (
                edge_data.get(
                    "relationship_id",
                    edge_key,
                )
            )

            reachable_relationship_ids.append(
                int(
                    relationship_id
                )
            )


    reachable_relationship_ids.sort()


    max_hops = max(
        (
            result.hop_count
            for result in path_results
        ),
        default=0,
    )


    return ReachabilityResult(
        start_asset_id=start_asset_id,

        reachable_asset_ids=(
            ordered_reachable_asset_ids
        ),

        reachable_relationship_ids=tuple(
            reachable_relationship_ids
        ),

        paths=tuple(
            path_results
        ),

        max_hops=max_hops,
    )
