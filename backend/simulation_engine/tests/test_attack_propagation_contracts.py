import unittest

import networkx as nx

from simulation_engine.attack_propagation import (
    analyze_attack_propagation,
)


class AttackPropagationContractTests(
    unittest.TestCase
):
    def test_unknown_start_asset_is_rejected(
        self,
    ):
        graph = (
            nx.MultiDiGraph()
        )


        with self.assertRaises(
            ValueError
        ):
            analyze_attack_propagation(
                graph=graph,
                vulnerabilities=(),
                start_asset_id=999,
                start_privilege="LOW",
            )


    def test_invalid_start_privilege_is_rejected(
        self,
    ):
        graph = (
            nx.MultiDiGraph()
        )

        graph.add_node(
            1
        )


        with self.assertRaises(
            ValueError
        ):
            analyze_attack_propagation(
                graph=graph,
                vulnerabilities=(),
                start_asset_id=1,
                start_privilege="ADMIN",
            )


    def test_connectivity_alone_does_not_imply_compromise(
        self,
    ):
        graph = (
            nx.MultiDiGraph()
        )


        graph.add_node(
            1
        )

        graph.add_node(
            2
        )


        graph.add_edge(
            1,
            2,
            key=10,
            relationship_id=10,
            required_source_privilege=(
                "LOW"
            ),
            requires_authentication=(
                False
            ),
            requires_mfa=False,
        )


        result = (
            analyze_attack_propagation(
                graph=graph,
                vulnerabilities=(),
                start_asset_id=1,
                start_privilege="LOW",
            )
        )


        propagated_asset_ids = {
            propagated.asset_id

            for propagated
            in result.propagated_assets
        }


        self.assertNotIn(
            2,
            propagated_asset_ids,
        )


    def test_same_input_produces_same_result(
        self,
    ):
        graph = (
            nx.MultiDiGraph()
        )

        graph.add_node(
            1
        )


        first_result = (
            analyze_attack_propagation(
                graph=graph,
                vulnerabilities=(),
                start_asset_id=1,
                start_privilege="LOW",
            )
        )


        second_result = (
            analyze_attack_propagation(
                graph=graph,
                vulnerabilities=(),
                start_asset_id=1,
                start_privilege="LOW",
            )
        )


        self.assertEqual(
            first_result,
            second_result,
        )


    def test_engine_does_not_mutate_input_graph(
        self,
    ):
        graph = (
            nx.MultiDiGraph()
        )


        graph.add_node(
            1,
            name="Source",
        )

        graph.add_node(
            2,
            name="Target",
        )


        graph.add_edge(
            1,
            2,
            key=10,
            relationship_id=10,
            required_source_privilege=(
                "LOW"
            ),
            requires_authentication=(
                False
            ),
            requires_mfa=False,
        )


        nodes_before = list(
            graph.nodes(
                data=True
            )
        )

        edges_before = list(
            graph.edges(
                keys=True,
                data=True,
            )
        )


        analyze_attack_propagation(
            graph=graph,
            vulnerabilities=(),
            start_asset_id=1,
            start_privilege="LOW",
        )


        nodes_after = list(
            graph.nodes(
                data=True
            )
        )

        edges_after = list(
            graph.edges(
                keys=True,
                data=True,
            )
        )


        self.assertEqual(
            nodes_before,
            nodes_after,
        )

        self.assertEqual(
            edges_before,
            edges_after,
        )


if __name__ == "__main__":
    unittest.main()
