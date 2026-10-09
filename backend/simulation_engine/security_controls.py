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
    analyze_counterfactual,
)

from .records import (
    VulnerabilityRecord,
)


@dataclass(
    frozen=True,
    slots=True,
)
class CompiledControlModifications:
    disabled_relationship_ids: tuple[
        int,
        ...,
    ]

    disabled_vulnerability_ids: tuple[
        int,
        ...,
    ]

    force_authentication_relationship_ids: tuple[
        int,
        ...,
    ]

    force_mfa_relationship_ids: tuple[
        int,
        ...,
    ]

    high_privilege_relationship_ids: tuple[
        int,
        ...,
    ]


@dataclass(
    frozen=True,
    slots=True,
)
class SecurityControlSimulationResult:
    modifications: (
        CompiledControlModifications
    )

    comparison: (
        CounterfactualComparison
    )


def compile_security_controls(
    controls: tuple[
        SecurityControlRecord,
        ...,
    ],
) -> CompiledControlModifications:
    disabled_relationship_ids = set()

    disabled_vulnerability_ids = set()

    force_authentication_relationship_ids = (
        set()
    )

    force_mfa_relationship_ids = set()

    high_privilege_relationship_ids = set()


    for control in controls:
        if (
            control.control_type
            == "NETWORK_SEGMENTATION"
        ):
            if (
                control.target_relationship_id
                is None
            ):
                raise ValueError(
                    "Network segmentation "
                    "requires a target "
                    "relationship."
                )

            disabled_relationship_ids.add(
                control
                .target_relationship_id
            )


        elif (
            control.control_type
            == "VULNERABILITY_REMEDIATION"
        ):
            if (
                control.target_vulnerability_id
                is None
            ):
                raise ValueError(
                    "Vulnerability remediation "
                    "requires a target "
                    "vulnerability."
                )

            disabled_vulnerability_ids.add(
                control
                .target_vulnerability_id
            )


        elif (
            control.control_type
            == "MFA"
        ):
            if (
                control.target_relationship_id
                is None
            ):
                raise ValueError(
                    "MFA requires a target "
                    "relationship."
                )

            force_mfa_relationship_ids.add(
                control
                .target_relationship_id
            )


        elif (
            control.control_type
            == "LEAST_PRIVILEGE"
        ):
            if (
                control.target_relationship_id
                is None
            ):
                raise ValueError(
                    "Least privilege requires "
                    "a target relationship."
                )

            high_privilege_relationship_ids.add(
                control
                .target_relationship_id
            )


        elif (
            control.control_type
            == "AUTHENTICATION_ENFORCEMENT"
        ):
            if (
                control.target_relationship_id
                is None
            ):
                raise ValueError(
                    "Authentication "
                    "enforcement requires a "
                    "target relationship."
                )

            force_authentication_relationship_ids.add(
                control
                .target_relationship_id
            )


        else:
            raise ValueError(
                "Unsupported security "
                f"control type: "
                f"{control.control_type}"
            )


    return CompiledControlModifications(
        disabled_relationship_ids=(
            tuple(
                sorted(
                    disabled_relationship_ids
                )
            )
        ),

        disabled_vulnerability_ids=(
            tuple(
                sorted(
                    disabled_vulnerability_ids
                )
            )
        ),

        force_authentication_relationship_ids=(
            tuple(
                sorted(
                    force_authentication_relationship_ids
                )
            )
        ),

        force_mfa_relationship_ids=(
            tuple(
                sorted(
                    force_mfa_relationship_ids
                )
            )
        ),

        high_privilege_relationship_ids=(
            tuple(
                sorted(
                    high_privilege_relationship_ids
                )
            )
        ),
    )


def analyze_security_controls(
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
) -> SecurityControlSimulationResult:
    modifications = (
        compile_security_controls(
            controls
        )
    )


    comparison = (
        analyze_counterfactual(
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

            start_asset_id=(
                start_asset_id
            ),

            start_privilege=(
                start_privilege
            ),

            disabled_relationship_ids=(
                modifications
                .disabled_relationship_ids
            ),

            disabled_vulnerability_ids=(
                modifications
                .disabled_vulnerability_ids
            ),

            force_authentication_relationship_ids=(
                modifications
                .force_authentication_relationship_ids
            ),

            force_mfa_relationship_ids=(
                modifications
                .force_mfa_relationship_ids
            ),

            high_privilege_relationship_ids=(
                modifications
                .high_privilege_relationship_ids
            ),
        )
    )


    return SecurityControlSimulationResult(
        modifications=modifications,

        comparison=comparison,
    )
