from collections.abc import Iterable

import networkx as nx

from .records import (
    AssetRecord,
    RelationshipRecord,
)


def build_topology_graph(
    assets: Iterable[AssetRecord],
    relationships: Iterable[
        RelationshipRecord
    ],
) -> nx.MultiDiGraph:
    graph = nx.MultiDiGraph()

    for asset in assets:
        graph.add_node(
            asset.id,
            name=asset.name,
            asset_type=asset.asset_type,
            criticality=asset.criticality,
            environment=asset.environment,
            network_zone_id=(
                asset.network_zone_id
            ),
            is_internet_exposed=(
                asset.is_internet_exposed
            ),
        )

    for relationship in relationships:
        if relationship.source_id not in graph:
            raise ValueError(
                "Relationship source asset "
                f"{relationship.source_id} "
                "does not exist in the graph."
            )

        if relationship.target_id not in graph:
            raise ValueError(
                "Relationship target asset "
                f"{relationship.target_id} "
                "does not exist in the graph."
            )

        graph.add_edge(
            relationship.source_id,
            relationship.target_id,
            key=relationship.id,
            relationship_id=(
                relationship.id
            ),
            relationship_type=(
                relationship.relationship_type
            ),
            protocol=(
                relationship.protocol
            ),
            port=relationship.port,
            requires_authentication=(
                relationship
                .requires_authentication
            ),

	    required_source_privilege=(
	        relationship
	        .required_source_privilege
	    ),
        )

    return graph
