from dataclasses import dataclass

import networkx as nx

from assets.models import (
    Asset,
    Relationship,
)

from organizations.models import (
    Organization,
)

from security.models import (
    Vulnerability,
)

from simulation_engine.graph_builder import (
    build_topology_graph,
)

from simulation_engine.records import (
    AssetRecord,
    RelationshipRecord,
    VulnerabilityRecord,
)


@dataclass(
    slots=True,
)
class OrganizationGraphContext:
    graph: nx.MultiDiGraph

    assets_by_id: dict[
        int,
        Asset,
    ]

    relationships_by_id: dict[
        int,
        Relationship,
    ]

    vulnerabilities_by_id: dict[
        int,
        Vulnerability,
    ]

    vulnerability_records: tuple[
        VulnerabilityRecord,
        ...,
    ]

def load_organization_graph(
    organization: Organization,
) -> OrganizationGraphContext:
    assets = list(
        Asset.objects.filter(
            organization=organization
        ).select_related(
            "organization",
            "network_zone",
        )
    )


    relationships = list(
        Relationship.objects.filter(
            source__organization=organization,
            target__organization=organization,
        ).select_related(
            "source",
            "target",
        )
    )

    vulnerabilities = list(
        Vulnerability.objects.filter(
            asset__organization=organization,
        ).select_related(
            "asset",
        )
    )

    asset_records = [
        AssetRecord(
            id=asset.id,

            name=asset.name,

            asset_type=(
                asset.asset_type
            ),

            criticality=(
                asset.criticality
            ),

            environment=(
                asset.environment
            ),

            network_zone_id=(
                asset.network_zone_id
            ),

            is_internet_exposed=(
                asset
                .is_internet_exposed
            ),
        )

        for asset in assets
    ]


    relationship_records = [
        RelationshipRecord(
            id=relationship.id,

            source_id=(
                relationship.source_id
            ),

            target_id=(
                relationship.target_id
            ),

	    required_source_privilege=(
	        relationship
	        .required_source_privilege
	    ),

            relationship_type=(
                relationship
                .relationship_type
            ),

            protocol=(
                relationship.protocol
            ),

            port=(
                relationship.port
            ),

            requires_authentication=(
                relationship
                .requires_authentication
            ),
        )

        for relationship
        in relationships
    ]

    vulnerability_records = [
        VulnerabilityRecord(
            id=vulnerability.id,

            asset_id=(
                vulnerability.asset_id
            ),

            title=(
                vulnerability.title
            ),

            reference_id=(
                vulnerability.reference_id
            ),

            attack_vector=(
                vulnerability.attack_vector
            ),

            privileges_required=(
                vulnerability
               .privileges_required
            ),

            grants_privilege=(
                vulnerability
                .grants_privilege
            ),

            bypasses_authentication=(
                vulnerability
                .bypasses_authentication
            ),

            is_exploitable=(
                vulnerability
                .is_exploitable
            ),
        )

        for vulnerability
        in vulnerabilities
    ]

    graph = build_topology_graph(
        assets=asset_records,
        relationships=(
            relationship_records
        ),
    )


    return OrganizationGraphContext(
        graph=graph,

        assets_by_id={
            asset.id: asset
            for asset in assets
        },

	vulnerabilities_by_id={
	    vulnerability.id:
	        vulnerability

	    for vulnerability
	    in vulnerabilities
	},

	vulnerability_records=tuple(
	    vulnerability_records
	),

        relationships_by_id={
            relationship.id:
                relationship

            for relationship
            in relationships
        },
    )
