from collections import defaultdict, deque
from dataclasses import dataclass

import networkx as nx

from .records import VulnerabilityRecord


PRIVILEGE_RANK = {
    "NONE": 0,
    "LOW": 1,
    "HIGH": 2,
}


@dataclass(
    frozen=True,
    slots=True,
)
class PropagatedAsset:
    asset_id: int

    privilege: str

    hop_count: int

    path_asset_ids: tuple[
        int,
        ...,
    ]

    path_relationship_ids: tuple[
        int,
        ...,
    ]

    via_vulnerability_id: (
        int | None
    )


@dataclass(
    frozen=True,
    slots=True,
)
class BlockedTransition:
    relationship_id: int

    source_asset_id: int
    target_asset_id: int

    reason_code: str
    reason: str


@dataclass(
    frozen=True,
    slots=True,
)
class AttackPropagationResult:
    start_asset_id: int
    start_privilege: str

    propagated_assets: tuple[
        PropagatedAsset,
        ...,
    ]

    traversed_relationship_ids: tuple[
        int,
        ...,
    ]

    exploited_vulnerability_ids: tuple[
        int,
        ...,
    ]

    blocked_transitions: tuple[
        BlockedTransition,
        ...,
    ]

    max_hops: int


def _privilege_rank(
    privilege: str,
) -> int:
    try:
        return PRIVILEGE_RANK[
            privilege
        ]
    except KeyError as exc:
        raise ValueError(
            "Unknown privilege level: "
            f"{privilege}"
        ) from exc


def _higher_privilege(
    first: str,
    second: str,
) -> str:
    if (
        _privilege_rank(first)
        >= _privilege_rank(second)
    ):
        return first

    return second


def _apply_local_escalation(
    asset_id: int,
    current_privilege: str,
    vulnerabilities_by_asset: dict[
        int,
        list[VulnerabilityRecord],
    ],
    exploited_vulnerability_ids: set[
        int
    ],
) -> str:
    privilege = current_privilege

    while True:
        candidates = [
            vulnerability

            for vulnerability
            in vulnerabilities_by_asset.get(
                asset_id,
                [],
            )

            if (
                vulnerability
                .is_exploitable

                and vulnerability
                .attack_vector
                == "LOCAL"

                and (
                    _privilege_rank(
                        privilege
                    )
                    >=
                    _privilege_rank(
                        vulnerability
                        .privileges_required
                    )
                )

                and (
                    _privilege_rank(
                        vulnerability
                        .grants_privilege
                    )
                    >
                    _privilege_rank(
                        privilege
                    )
                )
            )
        ]

        if not candidates:
            return privilege

        candidates.sort(
            key=lambda vulnerability: (
                -_privilege_rank(
                    vulnerability
                    .grants_privilege
                ),
                vulnerability.id,
            )
        )

        chosen = candidates[0]

        exploited_vulnerability_ids.add(
            chosen.id
        )

        privilege = (
            chosen.grants_privilege
        )


def _select_remote_vulnerability(
    graph: nx.MultiDiGraph,
    source_asset_id: int,
    target_asset_id: int,
    requires_authentication: bool,
    vulnerabilities_by_asset: dict[
        int,
        list[VulnerabilityRecord],
    ],
) -> tuple[
    VulnerabilityRecord | None,
    str,
    str,
]:
    vulnerabilities = [
        vulnerability

        for vulnerability
        in vulnerabilities_by_asset.get(
            target_asset_id,
            [],
        )

        if vulnerability.is_exploitable
    ]

    if not vulnerabilities:
        return (
            None,
            "NO_EXPLOITABLE_VULNERABILITY",
            (
                "Target has no modeled "
                "exploitable vulnerability."
            ),
        )

    remote_vulnerabilities = [
        vulnerability

        for vulnerability
        in vulnerabilities

        if vulnerability.attack_vector
        in {
            "NETWORK",
            "ADJACENT",
        }
    ]

    if not remote_vulnerabilities:
        return (
            None,
            "NO_REMOTE_VULNERABILITY",
            (
                "Target has no modeled "
                "Network or Adjacent "
                "vulnerability."
            ),
        )

    source_zone = (
        graph.nodes[
            source_asset_id
        ].get("network_zone_id")
    )

    target_zone = (
        graph.nodes[
            target_asset_id
        ].get("network_zone_id")
    )

    vector_eligible = []

    for vulnerability in (
        remote_vulnerabilities
    ):
        if (
            vulnerability.attack_vector
            == "NETWORK"
        ):
            vector_eligible.append(
                vulnerability
            )

            continue

        if (
            vulnerability.attack_vector
            == "ADJACENT"
            and source_zone is not None
            and source_zone
            == target_zone
        ):
            vector_eligible.append(
                vulnerability
            )

    if not vector_eligible:
        return (
            None,
            "ADJACENCY_REQUIREMENT_NOT_MET",
            (
                "Only Adjacent vulnerabilities "
                "are available and the source "
                "and target are not in the "
                "same modeled network zone."
            ),
        )

    no_prior_target_privilege = [
        vulnerability

        for vulnerability
        in vector_eligible

        if (
            vulnerability
            .privileges_required
            == "NONE"
        )
    ]

    if not no_prior_target_privilege:
        return (
            None,
            "TARGET_PRIVILEGE_REQUIRED",
            (
                "Available vulnerabilities "
                "require existing privilege "
                "on the target asset."
            ),
        )

    authentication_eligible = [
        vulnerability

        for vulnerability
        in no_prior_target_privilege

        if (
            not requires_authentication

            or vulnerability
            .bypasses_authentication
        )
    ]

    if not authentication_eligible:
        return (
            None,
            "AUTHENTICATION_REQUIRED",
            (
                "Relationship requires "
                "authentication and no "
                "eligible vulnerability "
                "is modeled as bypassing it."
            ),
        )

    authentication_eligible.sort(
        key=lambda vulnerability: (
            -_privilege_rank(
                vulnerability
                .grants_privilege
            ),
            vulnerability.id,
        )
    )

    return (
        authentication_eligible[0],
        "",
        "",
    )


def analyze_attack_propagation(
    graph: nx.MultiDiGraph,
    vulnerabilities: tuple[
        VulnerabilityRecord,
        ...,
    ],
    start_asset_id: int,
    start_privilege: str = "LOW",
) -> AttackPropagationResult:
    if start_asset_id not in graph:
        raise ValueError(
            "The start asset does not "
            "exist in the graph."
        )

    if start_privilege not in {
        "LOW",
        "HIGH",
    }:
        raise ValueError(
            "Start privilege must be "
            "LOW or HIGH."
        )

    vulnerabilities_by_asset: dict[
        int,
        list[VulnerabilityRecord],
    ] = defaultdict(list)

    for vulnerability in vulnerabilities:
        vulnerabilities_by_asset[
            vulnerability.asset_id
        ].append(
            vulnerability
        )

    exploited_vulnerability_ids: set[
        int
    ] = set()

    privileges: dict[
        int,
        str,
    ] = {}

    path_asset_ids: dict[
        int,
        tuple[int, ...],
    ] = {}

    path_relationship_ids: dict[
        int,
        tuple[int, ...],
    ] = {}

    via_vulnerability_id: dict[
        int,
        int | None,
    ] = {}

    start_effective_privilege = (
        _apply_local_escalation(
            start_asset_id,
            start_privilege,
            vulnerabilities_by_asset,
            exploited_vulnerability_ids,
        )
    )

    privileges[
        start_asset_id
    ] = start_effective_privilege

    path_asset_ids[
        start_asset_id
    ] = (
        start_asset_id,
    )

    path_relationship_ids[
        start_asset_id
    ] = ()

    via_vulnerability_id[
        start_asset_id
    ] = None

    queue = deque(
        [start_asset_id]
    )

    traversed_relationship_ids: set[
        int
    ] = set()

    while queue:
        source_asset_id = (
            queue.popleft()
        )

        source_privilege = (
            privileges[
                source_asset_id
            ]
        )

        for (
            _source,
            target_asset_id,
            edge_key,
            edge_data,
        ) in graph.out_edges(
            source_asset_id,
            keys=True,
            data=True,
        ):
            relationship_id = int(
                edge_data.get(
                    "relationship_id",
                    edge_key,
                )
            )

            required_source_privilege = (
                edge_data.get(
                    "required_source_privilege",
                    "LOW",
                )
            )

            if (
                _privilege_rank(
                    source_privilege
                )
                <
                _privilege_rank(
                    required_source_privilege
                )
            ):
                continue

            vulnerability, _, _ = (
                _select_remote_vulnerability(
                    graph=graph,

                    source_asset_id=(
                        source_asset_id
                    ),

                    target_asset_id=(
                        target_asset_id
                    ),

                    requires_authentication=(
                        bool(
                            edge_data.get(
                                "requires_authentication",
                                False,
                            )
                        )
                    ),

                    vulnerabilities_by_asset=(
                        vulnerabilities_by_asset
                    ),
                )
            )

            if vulnerability is None:
                continue

            traversed_relationship_ids.add(
                relationship_id
            )

            exploited_vulnerability_ids.add(
                vulnerability.id
            )

            new_privilege = (
                vulnerability
                .grants_privilege
            )

            new_privilege = (
                _apply_local_escalation(
                    target_asset_id,
                    new_privilege,
                    vulnerabilities_by_asset,
                    exploited_vulnerability_ids,
                )
            )

            existing_privilege = (
                privileges.get(
                    target_asset_id
                )
            )

            should_update = (
                existing_privilege is None

                or (
                    _privilege_rank(
                        new_privilege
                    )
                    >
                    _privilege_rank(
                        existing_privilege
                    )
                )
            )

            if not should_update:
                continue

            privileges[
                target_asset_id
            ] = (
                new_privilege
            )

            path_asset_ids[
                target_asset_id
            ] = (
                path_asset_ids[
                    source_asset_id
                ]
                + (
                    target_asset_id,
                )
            )

            path_relationship_ids[
                target_asset_id
            ] = (
                path_relationship_ids[
                    source_asset_id
                ]
                + (
                    relationship_id,
                )
            )

            via_vulnerability_id[
                target_asset_id
            ] = vulnerability.id

            queue.append(
                target_asset_id
            )

    blocked_transitions = []

    seen_blocked = set()

    for source_asset_id in privileges:
        source_privilege = (
            privileges[
                source_asset_id
            ]
        )

        for (
            _source,
            target_asset_id,
            edge_key,
            edge_data,
        ) in graph.out_edges(
            source_asset_id,
            keys=True,
            data=True,
        ):
            relationship_id = int(
                edge_data.get(
                    "relationship_id",
                    edge_key,
                )
            )

            if (
                relationship_id
                in traversed_relationship_ids
            ):
                continue

            required_source_privilege = (
                edge_data.get(
                    "required_source_privilege",
                    "LOW",
                )
            )

            if (
                _privilege_rank(
                    source_privilege
                )
                <
                _privilege_rank(
                    required_source_privilege
                )
            ):
                reason_code = (
                    "SOURCE_PRIVILEGE_INSUFFICIENT"
                )

                reason = (
                    "Current source privilege "
                    f"is {source_privilege}, "
                    "but this relationship "
                    "requires "
                    f"{required_source_privilege}."
                )
            else:
                (
                    vulnerability,
                    reason_code,
                    reason,
                ) = (
                    _select_remote_vulnerability(
                        graph=graph,

                        source_asset_id=(
                            source_asset_id
                        ),

                        target_asset_id=(
                            target_asset_id
                        ),

                        requires_authentication=(
                            bool(
                                edge_data.get(
                                    "requires_authentication",
                                    False,
                                )
                            )
                        ),

                        vulnerabilities_by_asset=(
                            vulnerabilities_by_asset
                        ),
                    )
                )

                if vulnerability is not None:
                    continue

            marker = (
                relationship_id,
                reason_code,
            )

            if marker in seen_blocked:
                continue

            seen_blocked.add(
                marker
            )

            blocked_transitions.append(
                BlockedTransition(
                    relationship_id=(
                        relationship_id
                    ),

                    source_asset_id=(
                        source_asset_id
                    ),

                    target_asset_id=(
                        target_asset_id
                    ),

                    reason_code=(
                        reason_code
                    ),

                    reason=reason,
                )
            )

    propagated_asset_ids = [
        asset_id

        for asset_id
        in privileges

        if asset_id
        != start_asset_id
    ]

    propagated_asset_ids.sort(
        key=lambda asset_id: (
            len(
                path_relationship_ids[
                    asset_id
                ]
            ),
            asset_id,
        )
    )

    propagated_assets = tuple(
        PropagatedAsset(
            asset_id=asset_id,

            privilege=(
                privileges[
                    asset_id
                ]
            ),

            hop_count=len(
                path_relationship_ids[
                    asset_id
                ]
            ),

            path_asset_ids=(
                path_asset_ids[
                    asset_id
                ]
            ),

            path_relationship_ids=(
                path_relationship_ids[
                    asset_id
                ]
            ),

            via_vulnerability_id=(
                via_vulnerability_id[
                    asset_id
                ]
            ),
        )

        for asset_id
        in propagated_asset_ids
    )

    max_hops = max(
        (
            asset.hop_count
            for asset
            in propagated_assets
        ),
        default=0,
    )

    return AttackPropagationResult(
        start_asset_id=(
            start_asset_id
        ),

        start_privilege=(
            start_effective_privilege
        ),

        propagated_assets=(
            propagated_assets
        ),

        traversed_relationship_ids=(
            tuple(
                sorted(
                    traversed_relationship_ids
                )
            )
        ),

        exploited_vulnerability_ids=(
            tuple(
                sorted(
                    exploited_vulnerability_ids
                )
            )
        ),

        blocked_transitions=(
            tuple(
                blocked_transitions
            )
        ),

        max_hops=max_hops,
    )
