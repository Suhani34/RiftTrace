from collections import (
    Counter,
    defaultdict,
)

from dataclasses import asdict

from .path_records import (
    AttackTransition,
    PathTargetMetadata,
)


def _state(
    asset_id,
    privilege,
):
    return (
        asset_id,
        privilege,
    )


def _is_important_target(
    metadata,
):
    return (
        metadata.criticality
        == "CRITICAL"

        or bool(
            metadata
            .critical_business_processes
        )
    )


def _build_default_targets(
    transitions,
    target_metadata,
):
    important_targets = {
        asset_id

        for (
            asset_id,
            metadata,
        )
        in target_metadata.items()

        if _is_important_target(
            metadata
        )
    }


    if important_targets:
        return important_targets


    return {
        transition.target_asset_id

        for transition
        in transitions
    }


def _path_assets(
    start_asset_id,
    start_asset_name,
    start_privilege,
    transitions,
):
    assets = [
        {
            "asset_id":
                start_asset_id,

            "asset_name":
                start_asset_name,

            "privilege":
                start_privilege,
        }
    ]


    for transition in transitions:
        assets.append(
            {
                "asset_id":
                    transition
                    .target_asset_id,

                "asset_name":
                    transition
                    .target_asset_name,

                "privilege":
                    transition
                    .target_privilege,
            }
        )


    return assets


def _create_path_record(
    path_number,
    start_asset_id,
    start_asset_name,
    start_privilege,
    transitions,
    target_metadata,
):
    final_transition = (
        transitions[-1]
    )


    target_asset_id = (
        final_transition
        .target_asset_id
    )


    metadata = (
        target_metadata.get(
            target_asset_id
        )
    )


    if metadata is None:
        metadata = (
            PathTargetMetadata(
                asset_id=(
                    target_asset_id
                ),

                asset_name=(
                    final_transition
                    .target_asset_name
                ),

                criticality="UNKNOWN",
            )
        )


    business_critical = bool(
        metadata
        .critical_business_processes
    )


    critical = (
        metadata.criticality
        == "CRITICAL"
    )


    return {
        "path_id":
            (
                f"P"
                f"{path_number:04d}"
            ),

        "hop_count":
            len(
                transitions
            ),

        "is_critical_path":
            critical,

        "is_business_critical_path":
            business_critical,

        "target": {
            "asset_id":
                metadata.asset_id,

            "asset_name":
                metadata.asset_name,

            "criticality":
                metadata.criticality,

            "business_processes":
                list(
                    metadata
                    .business_processes
                ),

            "critical_business_processes":
                list(
                    metadata
                    .critical_business_processes
                ),
        },

        "assets":
            _path_assets(
                start_asset_id,
                start_asset_name,
                start_privilege,
                transitions,
            ),

        "transitions": [
            asdict(
                transition
            )

            for transition
            in transitions
        ],
    }


def _node_chokepoints(
    paths,
    start_asset_id,
):
    path_count = len(
        paths
    )


    if path_count == 0:
        return []


    counts = Counter()
    critical_counts = Counter()
    names = {}


    for path in paths:
        assets = (
            path[
                "assets"
            ]
        )


        intermediate_assets = (
            assets[
                1:-1
            ]
        )


        seen = set()


        for asset in intermediate_assets:
            asset_id = (
                asset[
                    "asset_id"
                ]
            )


            if (
                asset_id
                == start_asset_id
            ):
                continue


            if asset_id in seen:
                continue


            seen.add(
                asset_id
            )


            names[
                asset_id
            ] = (
                asset[
                    "asset_name"
                ]
            )


            counts[
                asset_id
            ] += 1


            if (
                path[
                    "is_critical_path"
                ]

                or path[
                    "is_business_critical_path"
                ]
            ):
                critical_counts[
                    asset_id
                ] += 1


    result = []


    for (
        asset_id,
        count,
    ) in counts.items():
        coverage = (
            count
            / path_count
            * 100.0
        )


        result.append(
            {
                "asset_id":
                    asset_id,

                "asset_name":
                    names[
                        asset_id
                    ],

                "paths_through":
                    count,

                "total_paths":
                    path_count,

                "coverage_percent":
                    round(
                        coverage,
                        2,
                    ),

                "critical_paths_through":
                    critical_counts[
                        asset_id
                    ],

                "paths_removed_if_blocked":
                    count,

                "remaining_paths":
                    (
                        path_count
                        - count
                    ),

                "single_point_chokepoint":
                    (
                        count
                        == path_count
                    ),
            }
        )


    result.sort(
        key=lambda item: (
            -item[
                "critical_paths_through"
            ],

            -item[
                "paths_through"
            ],

            item[
                "asset_name"
            ],
        )
    )


    return result


def _edge_chokepoints(
    paths,
):
    path_count = len(
        paths
    )


    if path_count == 0:
        return []


    counts = Counter()
    critical_counts = Counter()
    metadata = {}


    for path in paths:
        seen = set()


        for transition in (
            path[
                "transitions"
            ]
        ):
            relationship_id = (
                transition[
                    "relationship_id"
                ]
            )


            metadata[
                relationship_id
            ] = {
                "relationship_id":
                    relationship_id,

                "source_asset_id":
                    transition[
                        "source_asset_id"
                    ],

                "source_asset_name":
                    transition[
                        "source_asset_name"
                    ],

                "target_asset_id":
                    transition[
                        "target_asset_id"
                    ],

                "target_asset_name":
                    transition[
                        "target_asset_name"
                    ],
            }


            if (
                relationship_id
                in seen
            ):
                continue


            seen.add(
                relationship_id
            )


            counts[
                relationship_id
            ] += 1


            if (
                path[
                    "is_critical_path"
                ]

                or path[
                    "is_business_critical_path"
                ]
            ):
                critical_counts[
                    relationship_id
                ] += 1


    result = []


    for (
        relationship_id,
        count,
    ) in counts.items():
        coverage = (
            count
            / path_count
            * 100.0
        )


        item = {
            **metadata[
                relationship_id
            ],

            "paths_through":
                count,

            "total_paths":
                path_count,

            "coverage_percent":
                round(
                    coverage,
                    2,
                ),

            "critical_paths_through":
                critical_counts[
                    relationship_id
                ],

            "paths_removed_if_blocked":
                count,

            "remaining_paths":
                (
                    path_count
                    - count
                ),

            "single_point_chokepoint":
                (
                    count
                    == path_count
                ),
        }


        result.append(
            item
        )


    result.sort(
        key=lambda item: (
            -item[
                "critical_paths_through"
            ],

            -item[
                "paths_through"
            ],

            item[
                "relationship_id"
            ],
        )
    )


    return result


def analyze_attack_paths(
    *,
    start_asset_id,
    start_asset_name,
    start_privilege,
    transitions,
    target_metadata,
    target_asset_ids=None,
    max_depth=8,
    max_paths=1000,
):
    if max_depth < 1:
        raise ValueError(
            (
                "max_depth must "
                "be at least 1."
            )
        )


    if max_paths < 1:
        raise ValueError(
            (
                "max_paths must "
                "be at least 1."
            )
        )


    transitions = tuple(
        transitions
    )


    adjacency = defaultdict(
        list
    )


    for transition in transitions:
        adjacency[
            _state(
                transition
                .source_asset_id,

                transition
                .source_privilege,
            )
        ].append(
            transition
        )


    for transition_list in (
        adjacency.values()
    ):
        transition_list.sort(
            key=lambda item: (
                item.target_asset_id,
                item.target_privilege,
                item.relationship_id,
                (
                    item.vulnerability_id
                    if (
                        item
                        .vulnerability_id
                        is not None
                    )
                    else -1
                ),
            )
        )


    if target_asset_ids:
        targets = set(
            target_asset_ids
        )

    else:
        targets = (
            _build_default_targets(
                transitions,
                target_metadata,
            )
        )


    start_state = _state(
        start_asset_id,
        start_privilege,
    )


    paths = []

    limit_reached = False


    def walk(
        current_state,
        visited_states,
        transition_path,
    ):
        nonlocal limit_reached


        if (
            len(
                paths
            )
            >= max_paths
        ):
            limit_reached = True
            return


        current_asset_id = (
            current_state[
                0
            ]
        )


        if (
            transition_path

            and current_asset_id
            in targets
        ):
            paths.append(
                _create_path_record(
                    len(
                        paths
                    )
                    + 1,

                    start_asset_id,
                    start_asset_name,
                    start_privilege,
                    tuple(
                        transition_path
                    ),
                    target_metadata,
                )
            )


            if (
                len(
                    paths
                )
                >= max_paths
            ):
                limit_reached = True
                return


        if (
            len(
                transition_path
            )
            >= max_depth
        ):
            return


        for transition in (
            adjacency.get(
                current_state,
                ()
            )
        ):
            next_state = _state(
                transition
                .target_asset_id,

                transition
                .target_privilege,
            )


            if (
                next_state
                in visited_states
            ):
                continue


            walk(
                next_state,

                (
                    visited_states
                    | {
                        next_state
                    }
                ),

                (
                    transition_path
                    + [
                        transition
                    ]
                ),
            )


            if limit_reached:
                return


    walk(
        start_state,
        {
            start_state
        },
        [],
    )


    node_chokepoints = (
        _node_chokepoints(
            paths,
            start_asset_id,
        )
    )


    edge_chokepoints = (
        _edge_chokepoints(
            paths
        )
    )


    critical_paths = sum(
        1

        for path
        in paths

        if path[
            "is_critical_path"
        ]
    )


    business_critical_paths = sum(
        1

        for path
        in paths

        if path[
            "is_business_critical_path"
        ]
    )


    unique_targets = {
        path[
            "target"
        ][
            "asset_id"
        ]

        for path
        in paths
    }


    return {
        "summary": {
            "start_asset_id":
                start_asset_id,

            "start_asset_name":
                start_asset_name,

            "start_privilege":
                start_privilege,

            "target_count":
                len(
                    unique_targets
                ),

            "attack_paths":
                len(
                    paths
                ),

            "critical_attack_paths":
                critical_paths,

            "business_critical_attack_paths":
                business_critical_paths,

            "node_chokepoints":
                len(
                    node_chokepoints
                ),

            "edge_chokepoints":
                len(
                    edge_chokepoints
                ),

            "max_depth":
                max_depth,

            "max_paths":
                max_paths,

            "path_limit_reached":
                limit_reached,
        },

        "paths":
            paths,

        "node_chokepoints":
            node_chokepoints,

        "edge_chokepoints":
            edge_chokepoints,

        "interpretation": (
            "Paths and chokepoints describe "
            "potential propagation routes "
            "within the modeled RiftTrace "
            "environment. They do not "
            "represent observed attacker "
            "activity or guaranteed real-"
            "world compromise."
        ),
    }
