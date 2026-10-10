from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from assets.models import (
    Asset,
    Relationship,
)
from assets.serializers import (
    AssetSerializer,
    RelationshipSerializer,
)

from business.serializers import (
    BusinessProcessSerializer,
)

from simulation_engine.business_impact import (
    analyze_business_impact,
)

from simulation_engine.prioritization import (
    rank_security_controls,
)

from simulation_engine.security_controls import (
    analyze_security_controls,
)

from organizations.serializers import (
    OrganizationSerializer,
)

from security.models import (
    Vulnerability,
)

from security.serializers import (
    SecurityControlSerializer,
    VulnerabilitySerializer,
)

from simulation_engine.counterfactual import (
    analyze_counterfactual,
)

from simulation_engine.attack_propagation import (
    analyze_attack_propagation,
)

from .serializers import (
    AttackPropagationRequestSerializer,
    ReachabilitySimulationRequestSerializer,
    CounterfactualSimulationRequestSerializer,
    SecurityControlSimulationRequestSerializer,
    SecurityControlRankingRequestSerializer,
)

from simulation_engine.reachability import (
    analyze_reachability,
)

from .services import (
    load_business_context,
    load_organization_graph,
    load_security_control_context,
)

def _serialize_counterfactual_run(
    run,
    graph_context,
    business_context,
):
    propagated_assets = [
	{
            "asset":
                AssetSerializer(
                    graph_context
                    .assets_by_id[
                        propagated.asset_id
                    ]
                ).data,

            "privilege":
                propagated.privilege,

            "hop_count":
                propagated.hop_count,
        }

        for propagated
        in run
        .propagation
        .propagated_assets
    ]


    impacted_processes = [
        {
            "business_process":
                BusinessProcessSerializer(
                    business_context
                    .processes_by_id[
                        impact
                        .business_process_id
                    ]
                ).data,

            "strongest_dependency_level":
                impact
                .strongest_dependency_level,

            "affected_asset_ids":
                list(
                    impact
                    .affected_asset_ids
                ),

            "affected_assets": [
                AssetSerializer(
                    graph_context
                    .assets_by_id[
                        asset_id
                    ]
                ).data

                for asset_id
                in (
                    impact
                    .affected_asset_ids
                )
            ],
        }

        for impact
        in run
        .business_impact
        .impacted_processes
    ]


    critical_asset_count = sum(
        1

        for asset_id
        in run.affected_asset_ids

        if (
            graph_context
            .graph
            .nodes[
                asset_id
            ]
            .get("criticality")
            == "CRITICAL"
        )
    )


    return {
        "technical_consequence": {
            "affected_asset_ids":
                list(
                    run.affected_asset_ids
                ),

            "propagated_asset_ids": [
                propagated.asset_id

                for propagated
                in run
                .propagation
                .propagated_assets
            ],

            "propagated_asset_count":
                len(
                    run
                    .propagation
                    .propagated_assets
                ),

            "critical_asset_count":
                critical_asset_count,

            "traversed_relationship_ids":
                list(
                    run
                    .propagation
                    .traversed_relationship_ids
                ),

            "exploited_vulnerability_ids":
                list(
                    run
                    .propagation
                    .exploited_vulnerability_ids
                ),

            "max_hops":
                run
                .propagation
                .max_hops,

            "propagated_assets":
                propagated_assets,
        },

        "business_impact": {
            "summary": {
                "impacted_process_count":
                    run
                    .business_impact
                    .impacted_process_count,

                "critical_process_count":
                    run
                    .business_impact
                    .critical_process_count,

                "essential_dependency_hit_count":
                    run
                    .business_impact
                    .essential_dependency_hit_count,
            },

            "impacted_processes":
                impacted_processes,
        },
    }

def _serialize_comparison(
    comparison,
    graph_context,
    business_context,
):
    prevented_assets = [
        AssetSerializer(
            graph_context
            .assets_by_id[
                asset_id
            ]
        ).data

        for asset_id
        in (
            comparison
            .prevented_propagated_asset_ids
        )
    ]


    prevented_critical_assets = [
        AssetSerializer(
            graph_context
            .assets_by_id[
                asset_id
            ]
        ).data

        for asset_id
        in (
            comparison
            .prevented_critical_asset_ids
        )
    ]


    avoided_processes = [
        BusinessProcessSerializer(
            business_context
            .processes_by_id[
                process_id
            ]
        ).data

        for process_id
        in (
            comparison
            .avoided_business_process_ids
        )
    ]


    return {
        "propagated_asset_reduction":
            comparison
            .propagated_asset_reduction,

        "critical_asset_reduction":
            comparison
            .critical_asset_reduction,

        "impacted_process_reduction":
            comparison
            .impacted_process_reduction,

        "critical_process_reduction":
            comparison
            .critical_process_reduction,

        "essential_dependency_hit_reduction":
            comparison
            .essential_dependency_hit_reduction,

        "prevented_propagated_asset_ids":
            list(
                comparison
                .prevented_propagated_asset_ids
            ),

        "prevented_propagated_assets":
            prevented_assets,

        "prevented_critical_asset_ids":
            list(
                comparison
                .prevented_critical_asset_ids
            ),

        "prevented_critical_assets":
            prevented_critical_assets,

        "avoided_business_process_ids":
            list(
                comparison
                .avoided_business_process_ids
            ),

        "avoided_business_processes":
            avoided_processes,

        "prevented_traversed_relationship_ids":
            list(
                comparison
                .prevented_traversed_relationship_ids
            ),

        "prevented_exploited_vulnerability_ids":
            list(
                comparison
                .prevented_exploited_vulnerability_ids
            ),
    }

def _build_priority_reason(
    metrics,
):
    reasons = []


    if (
        metrics
        .critical_process_reduction
    ):
        reasons.append(
            (
                f"{metrics.critical_process_reduction} "
                "critical business "
                "process(es) avoided"
            )
        )


    if (
        metrics
        .critical_asset_reduction
    ):
        reasons.append(
            (
                f"{metrics.critical_asset_reduction} "
                "critical asset(s) "
                "prevented"
            )
        )


    if (
        metrics
        .essential_dependency_hit_reduction
    ):
        reasons.append(
            (
                f"{metrics.essential_dependency_hit_reduction} "
                "essential dependency "
                "hit(s) prevented"
            )
        )


    if (
        metrics
        .impacted_process_reduction
    ):
        reasons.append(
            (
                f"{metrics.impacted_process_reduction} "
                "business process(es) "
                "avoided"
            )
        )


    if (
        metrics
        .propagated_asset_reduction
    ):
        reasons.append(
            (
                f"{metrics.propagated_asset_reduction} "
                "propagated asset(s) "
                "prevented"
            )
        )


    if not reasons:
        return (
            "No measured consequence "
            "reduction for this modeled "
            "scenario."
        )


    return "; ".join(
        reasons
    ) + "."

class ReachabilitySimulationView(
    APIView
):
    def post(self, request):
        serializer = (
            ReachabilitySimulationRequestSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )


        organization = (
            serializer.validated_data[
                "organization"
            ]
        )

        start_asset = (
            serializer.validated_data[
                "start_asset"
            ]
        )


        context = (
            load_organization_graph(
                organization
            )
        )


        result = analyze_reachability(
            graph=context.graph,

            start_asset_id=(
                start_asset.id
            ),
        )


        reachable_assets = []


        for path_result in result.paths:
            asset = (
                context.assets_by_id[
                    path_result.asset_id
                ]
            )


            path_names = [
                context.assets_by_id[
                    asset_id
                ].name

                for asset_id
                in (
                    path_result
                    .path_asset_ids
                )
            ]


            reachable_assets.append(
                {
                    "asset":
                        AssetSerializer(
                            asset
                        ).data,

                    "hop_count":
                        path_result
                        .hop_count,

                    "shortest_path_asset_ids":
                        list(
                            path_result
                            .path_asset_ids
                        ),

                    "shortest_path_asset_names":
                        path_names,
                }
            )


        reachable_critical_count = sum(
            1

            for asset_id
            in result.reachable_asset_ids

            if (
                context.assets_by_id[
                    asset_id
                ].criticality
                == Asset.Criticality.CRITICAL
            )
        )


        response_data = {
            "simulation_type":
                "topology_reachability",

            "organization":
                OrganizationSerializer(
                    organization
                ).data,

            "start_asset":
                AssetSerializer(
                    start_asset
                ).data,

            "summary": {
                "total_assets":
                    context.graph
                    .number_of_nodes(),

                "reachable_asset_count":
                    len(
                        result
                        .reachable_asset_ids
                    ),

                "reachable_critical_asset_count":
                    reachable_critical_count,

                "max_hops":
                    result.max_hops,
            },

            "reachable_asset_ids":
                list(
                    result
                    .reachable_asset_ids
                ),

            "reachable_relationship_ids":
                list(
                    result
                    .reachable_relationship_ids
                ),

            "reachable_assets":
                reachable_assets,

            "semantics": (
                "Topology-only reachability. "
                "A reachable asset is connected "
                "through directed modeled "
                "relationships from the selected "
                "start asset. This does not yet "
                "mean that an attacker can exploit "
                "or compromise that asset."
            ),
        }


        return Response(
            response_data,
            status=status.HTTP_200_OK,
        )

class AttackPropagationView(
    APIView
):
    def post(self, request):
        serializer = (
            AttackPropagationRequestSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        organization = (
            serializer.validated_data[
                "organization"
            ]
        )

        start_asset = (
            serializer.validated_data[
                "start_asset"
            ]
        )

        start_privilege = (
            serializer.validated_data[
                "start_privilege"
            ]
        )

        context = (
            load_organization_graph(
                organization
            )
        )

        result = (
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

        propagated_assets = []

        for propagated in (
            result.propagated_assets
        ):
            asset = (
                context.assets_by_id[
                    propagated.asset_id
                ]
            )

            path_names = [
                context.assets_by_id[
                    asset_id
                ].name

                for asset_id
                in (
                    propagated
                    .path_asset_ids
                )
            ]

            vulnerability = (
                context
                .vulnerabilities_by_id
                .get(
                    propagated
                    .via_vulnerability_id
                )
            )

            propagated_assets.append(
                {
                    "asset":
                        AssetSerializer(
                            asset
                        ).data,

                    "privilege":
                        propagated
                        .privilege,

                    "hop_count":
                        propagated
                        .hop_count,

                    "path_asset_ids":
                        list(
                            propagated
                            .path_asset_ids
                        ),

                    "path_asset_names":
                        path_names,

                    "path_relationship_ids":
                        list(
                            propagated
                            .path_relationship_ids
                        ),

                    "via_vulnerability": (
                        VulnerabilitySerializer(
                            vulnerability
                        ).data

                        if vulnerability
                        else None
                    ),
                }
            )

        propagated_ids = {
            item.asset_id
            for item
            in result.propagated_assets
        }

        critical_count = sum(
            1

            for asset_id
            in propagated_ids

            if (
                context.assets_by_id[
                    asset_id
                ].criticality
                == Asset.Criticality.CRITICAL
            )
        )

        blocked_transitions = []

        for blocked in (
            result.blocked_transitions
        ):
            blocked_transitions.append(
                {
                    "relationship_id":
                        blocked
                        .relationship_id,

                    "source_asset_id":
                        blocked
                        .source_asset_id,

                    "source_asset_name":
                        context.assets_by_id[
                            blocked
                            .source_asset_id
                        ].name,

                    "target_asset_id":
                        blocked
                        .target_asset_id,

                    "target_asset_name":
                        context.assets_by_id[
                            blocked
                            .target_asset_id
                        ].name,

                    "reason_code":
                        blocked.reason_code,

                    "reason":
                        blocked.reason,
                }
            )

        exploited_vulnerabilities = [
            VulnerabilitySerializer(
                context
                .vulnerabilities_by_id[
                    vulnerability_id
                ]
            ).data

            for vulnerability_id
            in (
                result
                .exploited_vulnerability_ids
            )

            if vulnerability_id
            in (
                context
                .vulnerabilities_by_id
            )
        ]

        response_data = {
            "simulation_type":
                "security_aware_propagation",

            "organization":
                OrganizationSerializer(
                    organization
                ).data,

            "start_asset":
                AssetSerializer(
                    start_asset
                ).data,

            "start_privilege":
                result.start_privilege,

            "summary": {
                "total_assets":
                    context.graph
                    .number_of_nodes(),

                "propagated_asset_count":
                    len(
                        result
                        .propagated_assets
                    ),

                "propagated_critical_asset_count":
                    critical_count,

                "max_hops":
                    result.max_hops,

                "blocked_transition_count":
                    len(
                        result
                        .blocked_transitions
                    ),
            },

            "propagated_asset_ids": [
                asset.asset_id

                for asset
                in result.propagated_assets
            ],

            "traversed_relationship_ids":
                list(
                    result
                    .traversed_relationship_ids
                ),

            "exploited_vulnerability_ids":
                list(
                    result
                    .exploited_vulnerability_ids
                ),

            "exploited_vulnerabilities":
                exploited_vulnerabilities,

            "propagated_assets":
                propagated_assets,

            "blocked_transitions":
                blocked_transitions,

            "semantics": (
                "Security-aware modeled "
                "propagation. Results depend "
                "on explicitly modeled "
                "relationships, privileges, "
                "vulnerabilities and "
                "authentication conditions. "
                "They represent potential "
                "scenario consequences, not "
                "a prediction that a real "
                "attack will succeed."
            ),
        }

        return Response(
            response_data,
            status=status.HTTP_200_OK,
        )

class BusinessImpactSimulationView(
    APIView
):
    def post(self, request):
        serializer = (
            AttackPropagationRequestSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )


        organization = (
            serializer.validated_data[
                "organization"
            ]
        )

        start_asset = (
            serializer.validated_data[
                "start_asset"
            ]
        )

        start_privilege = (
            serializer.validated_data[
                "start_privilege"
            ]
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


        propagation_result = (
            analyze_attack_propagation(
                graph=(
                    graph_context.graph
                ),

                vulnerabilities=(
                    graph_context
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


        affected_asset_ids = {
            start_asset.id,

            *(
                propagated.asset_id

                for propagated
                in (
                    propagation_result
                    .propagated_assets
                )
            ),
        }


        business_result = (
            analyze_business_impact(
                business_processes=(
                    business_context
                    .process_records
                ),

                dependencies=(
                    business_context
                    .dependency_records
                ),

                affected_asset_ids=(
                    affected_asset_ids
                ),
            )
        )


        propagated_assets = []

        for propagated in (
            propagation_result
            .propagated_assets
        ):
            asset = (
                graph_context
                .assets_by_id[
                    propagated.asset_id
                ]
            )

            propagated_assets.append(
                {
                    "asset":
                        AssetSerializer(
                            asset
                        ).data,

                    "privilege":
                        propagated
                        .privilege,

                    "hop_count":
                        propagated
                        .hop_count,
                }
            )


        impacted_processes = []

        for impact in (
            business_result
            .impacted_processes
        ):
            process = (
                business_context
                .processes_by_id[
                    impact
                    .business_process_id
                ]
            )


            affected_assets = [
                AssetSerializer(
                    graph_context
                    .assets_by_id[
                        asset_id
                    ]
                ).data

                for asset_id
                in (
                    impact
                    .affected_asset_ids
                )
            ]


            impacted_processes.append(
                {
                    "business_process":
                        BusinessProcessSerializer(
                            process
                        ).data,

                    "strongest_dependency_level":
                        impact
                        .strongest_dependency_level,

                    "affected_asset_ids":
                        list(
                            impact
                            .affected_asset_ids
                        ),

                    "affected_assets":
                        affected_assets,

                    "affected_dependency_ids":
                        list(
                            impact
                            .affected_dependency_ids
                        ),
                }
            )


        response_data = {
            "simulation_type":
                "business_impact",

            "organization":
                OrganizationSerializer(
                    organization
                ).data,

            "start_asset":
                AssetSerializer(
                    start_asset
                ).data,

            "start_privilege":
                propagation_result
                .start_privilege,

            "technical_consequence": {
                "affected_asset_ids":
                    sorted(
                        affected_asset_ids
                    ),

                "propagated_asset_ids": [
                    propagated.asset_id

                    for propagated
                    in (
                        propagation_result
                        .propagated_assets
                    )
                ],

                "traversed_relationship_ids":
                    list(
                        propagation_result
                        .traversed_relationship_ids
                    ),

                "propagated_assets":
                    propagated_assets,

                "blocked_transition_count":
                    len(
                        propagation_result
                        .blocked_transitions
                    ),
            },

            "business_impact": {
                "summary": {
                    "impacted_process_count":
                        business_result
                        .impacted_process_count,

                    "critical_process_count":
                        business_result
                        .critical_process_count,

                    "essential_dependency_hit_count":
                        business_result
                        .essential_dependency_hit_count,
                },

                "impacted_processes":
                    impacted_processes,
            },

            "semantics": (
                "Potential business impact "
                "derived from explicitly "
                "modeled dependencies between "
                "technical assets and business "
                "processes. An impacted process "
                "is not a prediction of actual "
                "business outage."
            ),
        }


        return Response(
            response_data,
            status=status.HTTP_200_OK,
        )

class CounterfactualSimulationView(
    APIView
):
    def post(self, request):
        serializer = (
            CounterfactualSimulationRequestSerializer(
                data=request.data
            )
        )


        serializer.is_valid(
            raise_exception=True
        )


        organization = (
            serializer.validated_data[
                "organization"
            ]
        )


        start_asset = (
            serializer.validated_data[
                "start_asset"
            ]
        )


        start_privilege = (
            serializer.validated_data[
                "start_privilege"
            ]
        )


        disabled_relationship_ids = (
            tuple(
                serializer
                .validated_data[
                    "disabled_relationship_ids"
                ]
            )
        )


        disabled_vulnerability_ids = (
            tuple(
                serializer
                .validated_data[
                    "disabled_vulnerability_ids"
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


        comparison = (
            analyze_counterfactual(
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

                start_asset_id=(
                    start_asset.id
                ),

                start_privilege=(
                    start_privilege
                ),

                disabled_relationship_ids=(
                    disabled_relationship_ids
                ),

                disabled_vulnerability_ids=(
                    disabled_vulnerability_ids
                ),
            )
        )


        disabled_relationships = (
            Relationship.objects.filter(
                id__in=(
                    disabled_relationship_ids
                )
            )
            .select_related(
                "source",
                "target",
            )
            .order_by("id")
        )


        disabled_vulnerabilities = (
            Vulnerability.objects.filter(
                id__in=(
                    disabled_vulnerability_ids
                )
            )
            .select_related(
                "asset",
            )
            .order_by("id")
        )


        prevented_assets = [
            AssetSerializer(
                graph_context
                .assets_by_id[
                    asset_id
                ]
            ).data

            for asset_id
            in (
                comparison
                .prevented_propagated_asset_ids
            )
        ]


        prevented_critical_assets = [
            AssetSerializer(
                graph_context
                .assets_by_id[
                    asset_id
                ]
            ).data

            for asset_id
            in (
                comparison
                .prevented_critical_asset_ids
            )
        ]


        avoided_processes = [
            BusinessProcessSerializer(
                business_context
                .processes_by_id[
                    process_id
                ]
            ).data

            for process_id
            in (
                comparison
                .avoided_business_process_ids
            )
        ]


        response_data = {
            "simulation_type":
                "counterfactual_comparison",

            "organization":
                OrganizationSerializer(
                    organization
                ).data,

            "start_asset":
                AssetSerializer(
                    start_asset
                ).data,

            "start_privilege":
                start_privilege,

            "modifications": {
                "disabled_relationships": [
                    RelationshipSerializer(
                        relationship
                    ).data

                    for relationship
                    in disabled_relationships
                ],

                "disabled_vulnerabilities": [
                    VulnerabilitySerializer(
                        vulnerability
                    ).data

                    for vulnerability
                    in disabled_vulnerabilities
                ],
            },

            "baseline":
                _serialize_counterfactual_run(
                    comparison.baseline,
                    graph_context,
                    business_context,
                ),

            "counterfactual":
                _serialize_counterfactual_run(
                    comparison
                    .counterfactual,
                    graph_context,
                    business_context,
                ),

            "comparison": {
                "propagated_asset_reduction":
                    comparison
                    .propagated_asset_reduction,

                "critical_asset_reduction":
                    comparison
                    .critical_asset_reduction,

                "impacted_process_reduction":
                    comparison
                    .impacted_process_reduction,

                "critical_process_reduction":
                    comparison
                    .critical_process_reduction,

                "essential_dependency_hit_reduction":
                    comparison
                    .essential_dependency_hit_reduction,

                "prevented_propagated_asset_ids":
                    list(
                        comparison
                        .prevented_propagated_asset_ids
                    ),

                "prevented_propagated_assets":
                    prevented_assets,

                "prevented_critical_asset_ids":
                    list(
                        comparison
                        .prevented_critical_asset_ids
                    ),

                "prevented_critical_assets":
                    prevented_critical_assets,

                "avoided_business_process_ids":
                    list(
                        comparison
                        .avoided_business_process_ids
                    ),

                "avoided_business_processes":
                    avoided_processes,

                "prevented_traversed_relationship_ids":
                    list(
                        comparison
                        .prevented_traversed_relationship_ids
                    ),

                "prevented_exploited_vulnerability_ids":
                    list(
                        comparison
                        .prevented_exploited_vulnerability_ids
                    ),
            },

            "semantics": (
                "Counterfactual comparison "
                "between the currently modeled "
                "baseline and a temporary "
                "in-memory scenario. Selected "
                "relationships and "
                "vulnerabilities are not "
                "deleted or modified in the "
                "database."
            ),
        }


        return Response(
            response_data,
            status=status.HTTP_200_OK,
        )

class SecurityControlSimulationView(
    APIView
):
    def post(self, request):
        serializer = (
            SecurityControlSimulationRequestSerializer(
                data=request.data
            )
        )


        serializer.is_valid(
            raise_exception=True
        )


        organization = (
            serializer.validated_data[
                "organization"
            ]
        )


        start_asset = (
            serializer.validated_data[
                "start_asset"
            ]
        )


        start_privilege = (
            serializer.validated_data[
                "start_privilege"
            ]
        )


        control_ids = (
            serializer.validated_data[
                "control_ids"
            ]
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


        control_context = (
            load_security_control_context(
                organization,

                control_ids,
            )
        )


        result = (
            analyze_security_controls(
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

                start_privilege=(
                    start_privilege
                ),
            )
        )


        comparison = (
            result.comparison
        )


        applied_controls = [
            SecurityControlSerializer(
                control_context
                .controls_by_id[
                    control_id
                ]
            ).data

            for control_id
            in control_ids
        ]


        modifications = (
            result.modifications
        )


        response_data = {
            "simulation_type":
                "security_control_comparison",

            "organization":
                OrganizationSerializer(
                    organization
                ).data,

            "start_asset":
                AssetSerializer(
                    start_asset
                ).data,

            "start_privilege":
                start_privilege,

            "applied_controls":
                applied_controls,

            "applied_modifications": {
                "disabled_relationship_ids":
                    list(
                        modifications
                        .disabled_relationship_ids
                    ),

                "disabled_vulnerability_ids":
                    list(
                        modifications
                        .disabled_vulnerability_ids
                    ),

                "force_authentication_relationship_ids":
                    list(
                        modifications
                        .force_authentication_relationship_ids
                    ),

                "force_mfa_relationship_ids":
                    list(
                        modifications
                        .force_mfa_relationship_ids
                    ),

                "high_privilege_relationship_ids":
                    list(
                        modifications
                        .high_privilege_relationship_ids
                    ),
            },

            "baseline":
                _serialize_counterfactual_run(
                    comparison.baseline,

                    graph_context,

                    business_context,
                ),

            "counterfactual":
                _serialize_counterfactual_run(
                    comparison
                    .counterfactual,

                    graph_context,

                    business_context,
                ),

            "comparison":
                _serialize_comparison(
                    comparison,

                    graph_context,

                    business_context,
                ),

            "semantics": (
                "Security-control simulation "
                "compares the current modeled "
                "baseline with temporary "
                "defensive-control effects. "
                "The controls do not modify "
                "the stored topology, "
                "vulnerabilities or "
                "relationships."
            ),
        }


        return Response(
            response_data,

            status=status.HTTP_200_OK,
        )
class SecurityControlRankingView(
    APIView
):
    def post(self, request):
        serializer = (
            SecurityControlRankingRequestSerializer(
                data=request.data
            )
        )


        serializer.is_valid(
            raise_exception=True
        )


        organization = (
            serializer.validated_data[
                "organization"
            ]
        )


        start_asset = (
            serializer.validated_data[
                "start_asset"
            ]
        )


        start_privilege = (
            serializer.validated_data[
                "start_privilege"
            ]
        )


        control_ids = (
            serializer.validated_data[
                "control_ids"
            ]
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


        control_context = (
            load_security_control_context(
                organization,

                control_ids,
            )
        )


        ranking_result = (
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

                start_privilege=(
                    start_privilege
                ),
            )
        )


        rank_counts = {}


        for ranked in (
            ranking_result
            .ranked_controls
        ):
            rank_counts[
                ranked.priority_rank
            ] = (
                rank_counts.get(
                    ranked.priority_rank,
                    0,
                )
                + 1
            )


        ranked_controls = []


        for ranked in (
            ranking_result
            .ranked_controls
        ):
            control = (
                control_context
                .controls_by_id[
                    ranked.control_id
                ]
            )


            comparison = (
                ranked.comparison
            )


            ranked_controls.append(
                {
                    "rank":
                        ranked
                        .priority_rank,

                    "tied":
                        rank_counts[
                            ranked
                            .priority_rank
                        ]
                        > 1,

                    "has_measured_effect":
                        ranked
                        .has_measured_effect,

                    "control":
                        SecurityControlSerializer(
                            control
                        ).data,

                    "metrics": {
                        "critical_process_reduction":
                            ranked
                            .metrics
                            .critical_process_reduction,

                        "critical_asset_reduction":
                            ranked
                            .metrics
                            .critical_asset_reduction,

                        "essential_dependency_hit_reduction":
                            ranked
                            .metrics
                            .essential_dependency_hit_reduction,

                        "impacted_process_reduction":
                            ranked
                            .metrics
                            .impacted_process_reduction,

                        "propagated_asset_reduction":
                            ranked
                            .metrics
                            .propagated_asset_reduction,
                    },

                    "priority_reason":
                        _build_priority_reason(
                            ranked.metrics
                        ),

                    "controlled_scenario":
                        _serialize_counterfactual_run(
                            comparison
                            .counterfactual,

                            graph_context,

                            business_context,
                        ),

                    "comparison":
                        _serialize_comparison(
                            comparison,

                            graph_context,

                            business_context,
                        ),
                }
            )


        first_comparison = (
            ranking_result
            .ranked_controls[
                0
            ]
            .comparison
        )


        response_data = {
            "simulation_type":
                "security_control_ranking",

            "organization":
                OrganizationSerializer(
                    organization
                ).data,

            "start_asset":
                AssetSerializer(
                    start_asset
                ).data,

            "start_privilege":
                start_privilege,

            "candidate_control_count":
                len(
                    ranked_controls
                ),

            "ranking_method": {
                "strategy":
                    (
                        "Business-first "
                        "lexicographic ranking"
                    ),

                "priority_order": [
                    (
                        "Critical business "
                        "process reduction"
                    ),

                    (
                        "Critical asset "
                        "reduction"
                    ),

                    (
                        "Essential dependency "
                        "hit reduction"
                    ),

                    (
                        "Total impacted "
                        "business process "
                        "reduction"
                    ),

                    (
                        "Total propagated "
                        "asset reduction"
                    ),
                ],

                "tie_behavior":
                    (
                        "Controls with identical "
                        "reduction metrics receive "
                        "the same rank."
                    ),
            },

            "baseline":
                _serialize_counterfactual_run(
                    first_comparison
                    .baseline,

                    graph_context,

                    business_context,
                ),

            "ranked_controls":
                ranked_controls,

            "semantics": (
                "Candidate controls are ranked "
                "by measured consequence "
                "reduction in this specific "
                "modeled attack scenario. "
                "The ranking is not a universal "
                "security rating and does not "
                "include implementation cost, "
                "operational complexity or "
                "real-world exploit probability."
            ),
        }


        return Response(
            response_data,

            status=status.HTTP_200_OK,
        )
