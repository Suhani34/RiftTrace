from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from assets.models import Asset
from assets.serializers import (
    AssetSerializer,
)

from organizations.serializers import (
    OrganizationSerializer,
)

from simulation_engine.reachability import (
    analyze_reachability,
)

from .serializers import (
    ReachabilitySimulationRequestSerializer,
)

from .services import (
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
