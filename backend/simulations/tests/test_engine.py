from django.test import SimpleTestCase

import networkx as nx

from simulation_engine.graph_builder import (
    build_topology_graph,
)

from simulation_engine.reachability import (
    analyze_reachability,
)

from simulation_engine.records import (
    AssetRecord,
    RelationshipRecord,
)


class ReachabilityEngineTests(
    SimpleTestCase
):
    def setUp(self):
        self.assets = [
            AssetRecord(
                id=1,
                name="Web",
                asset_type="SERVER",
                criticality="HIGH",
                environment="PRODUCTION",
                network_zone_id=1,
                is_internet_exposed=True,
            ),

            AssetRecord(
                id=2,
                name="API",
                asset_type="API",
                criticality="HIGH",
                environment="PRODUCTION",
                network_zone_id=2,
                is_internet_exposed=False,
            ),

            AssetRecord(
                id=3,
                name="Database",
                asset_type="DATABASE",
                criticality="CRITICAL",
                environment="PRODUCTION",
                network_zone_id=3,
                is_internet_exposed=False,
            ),

            AssetRecord(
                id=4,
                name="File Server",
                asset_type="FILE_SERVER",
                criticality="HIGH",
                environment="PRODUCTION",
                network_zone_id=2,
                is_internet_exposed=False,
            ),

            AssetRecord(
                id=5,
                name="Isolated Server",
                asset_type="SERVER",
                criticality="MEDIUM",
                environment="PRODUCTION",
                network_zone_id=2,
                is_internet_exposed=False,
            ),
        ]


        self.relationships = [
            RelationshipRecord(
                id=101,
                source_id=1,
                target_id=2,
                relationship_type="CALLS",
                protocol="HTTPS",
                port=443,
                requires_authentication=True,
		required_source_privilege="LOW",
            ),

            RelationshipRecord(
                id=102,
                source_id=2,
                target_id=3,
                relationship_type="READS",
                protocol="TCP",
                port=5432,
                requires_authentication=True,
		required_source_privilege="LOW",
            ),

            RelationshipRecord(
                id=103,
                source_id=1,
                target_id=4,
                relationship_type="CONNECTS_TO",
                protocol="HTTPS",
                port=443,
                requires_authentication=True,
		required_source_privilege="LOW",
            ),

            RelationshipRecord(
                id=104,
                source_id=1,
                target_id=2,
                relationship_type="DEPENDS_ON",
                protocol="HTTPS",
                port=443,
                requires_authentication=False,
		required_source_privilege="LOW",
            ),
        ]


        self.graph = build_topology_graph(
            self.assets,
            self.relationships,
        )


    def test_graph_is_directed_multigraph(
        self,
    ):
        self.assertIsInstance(
            self.graph,
            nx.MultiDiGraph,
        )


    def test_multiple_relationships_are_preserved(
        self,
    ):
        self.assertEqual(
            self.graph.number_of_edges(
                1,
                2,
            ),
            2,
        )


    def test_reachability_from_web(
        self,
    ):
        result = analyze_reachability(
            self.graph,
            1,
        )

        self.assertEqual(
            set(
                result
                .reachable_asset_ids
            ),
            {2, 3, 4},
        )


    def test_shortest_path_hop_count(
        self,
    ):
        result = analyze_reachability(
            self.graph,
            1,
        )

        database_path = next(
            path

            for path
            in result.paths

            if path.asset_id == 3
        )

        self.assertEqual(
            database_path.hop_count,
            2,
        )

        self.assertEqual(
            database_path
            .path_asset_ids,
            (1, 2, 3),
        )


    def test_direction_is_respected(
        self,
    ):
        result = analyze_reachability(
            self.graph,
            3,
        )

        self.assertEqual(
            result
            .reachable_asset_ids,
            (),
        )


    def test_isolated_asset_reaches_nothing(
        self,
    ):
        result = analyze_reachability(
            self.graph,
            5,
        )

        self.assertEqual(
            result
            .reachable_asset_ids,
            (),
        )

        self.assertEqual(
            result.max_hops,
            0,
        )


    def test_missing_start_asset_is_rejected(
        self,
    ):
        with self.assertRaises(
            ValueError
        ):
            analyze_reachability(
                self.graph,
                999,
            )
