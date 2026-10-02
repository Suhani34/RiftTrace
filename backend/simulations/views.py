from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from assets.models import Asset
from assets.serializers import (
    AssetSerializer,
)

from business.serializers import (
    BusinessProcessSerializer,
)

from simulation_engine.business_impact import (
    analyze_business_impact,
)

from organizations.serializers import (
    OrganizationSerializer,
)

from security.serializers import (
    VulnerabilitySerializer,
)

from simulation_engine.attack_propagation import (
    analyze_attack_propagation,
)

from .serializers import (
    AttackPropagationRequestSerializer,
    ReachabilitySimulationRequestSerializer,
)

from simulation_engine.reachability import (
    analyze_reachability,
)

from .services import (
    load_business_context,
    load_organization_graph,
)


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
