from django.test import (
    SimpleTestCase,
)

from simulation_engine.path_intelligence import (
    analyze_attack_paths,
)

from simulation_engine.path_records import (
    AttackTransition,
    PathTargetMetadata,
)


class PathIntelligenceTests(
    SimpleTestCase
):
    def transition(
        self,
        relationship_id,
        source_id,
        source_name,
        target_id,
        target_name,
    ):
        return AttackTransition(
            relationship_id=(
                relationship_id
            ),

            source_asset_id=(
                source_id
            ),

            source_asset_name=(
                source_name
            ),

            source_privilege="LOW",

            target_asset_id=(
                target_id
            ),

            target_asset_name=(
                target_name
            ),

            target_privilege="LOW",

            mechanism=(
                "TEST_TRANSITION"
            ),
        )


    def test_multiple_paths_are_found(
        self,
    ):
        transitions = [
            self.transition(
                1,
                1,
                "A",
                2,
                "B",
            ),

            self.transition(
                2,
                2,
                "B",
                4,
                "D",
            ),

            self.transition(
                3,
                1,
                "A",
                3,
                "C",
            ),

            self.transition(
                4,
                3,
                "C",
                4,
                "D",
            ),
        ]


        metadata = {
            4:
                PathTargetMetadata(
                    asset_id=4,
                    asset_name="D",
                    criticality=(
                        "CRITICAL"
                    ),
                )
        }


        result = (
            analyze_attack_paths(
                start_asset_id=1,
                start_asset_name="A",
                start_privilege="LOW",
                transitions=transitions,
                target_metadata=(
                    metadata
                ),
            )
        )


        self.assertEqual(
            result[
                "summary"
            ][
                "attack_paths"
            ],
            2,
        )


        self.assertEqual(
            result[
                "summary"
            ][
                "critical_attack_paths"
            ],
            2,
        )


    def test_common_node_becomes_chokepoint(
        self,
    ):
        transitions = [
            self.transition(
                1,
                1,
                "A",
                2,
                "B",
            ),

            self.transition(
                2,
                2,
                "B",
                3,
                "C",
            ),

            self.transition(
                3,
                2,
                "B",
                4,
                "D",
            ),
        ]


        metadata = {
            3:
                PathTargetMetadata(
                    asset_id=3,
                    asset_name="C",
                    criticality=(
                        "CRITICAL"
                    ),
                ),

            4:
                PathTargetMetadata(
                    asset_id=4,
                    asset_name="D",
                    criticality=(
                        "CRITICAL"
                    ),
                ),
        }


        result = (
            analyze_attack_paths(
                start_asset_id=1,
                start_asset_name="A",
                start_privilege="LOW",
                transitions=transitions,
                target_metadata=(
                    metadata
                ),
            )
        )


        chokepoint = (
            result[
                "node_chokepoints"
            ][
                0
            ]
        )


        self.assertEqual(
            chokepoint[
                "asset_id"
            ],
            2,
        )


        self.assertEqual(
            chokepoint[
                "coverage_percent"
            ],
            100.0,
        )


        self.assertTrue(
            chokepoint[
                "single_point_chokepoint"
            ]
        )


    def test_common_edge_becomes_chokepoint(
        self,
    ):
        transitions = [
            self.transition(
                10,
                1,
                "A",
                2,
                "B",
            ),

            self.transition(
                11,
                2,
                "B",
                3,
                "C",
            ),

            self.transition(
                12,
                2,
                "B",
                4,
                "D",
            ),
        ]


        metadata = {
            3:
                PathTargetMetadata(
                    asset_id=3,
                    asset_name="C",
                    criticality=(
                        "CRITICAL"
                    ),
                ),

            4:
                PathTargetMetadata(
                    asset_id=4,
                    asset_name="D",
                    criticality=(
                        "CRITICAL"
                    ),
                ),
        }


        result = (
            analyze_attack_paths(
                start_asset_id=1,
                start_asset_name="A",
                start_privilege="LOW",
                transitions=transitions,
                target_metadata=(
                    metadata
                ),
            )
        )


        first_edge = (
            result[
                "edge_chokepoints"
            ][
                0
            ]
        )


        self.assertEqual(
            first_edge[
                "relationship_id"
            ],
            10,
        )


        self.assertEqual(
            first_edge[
                "coverage_percent"
            ],
            100.0,
        )


    def test_cycle_does_not_loop_forever(
        self,
    ):
        transitions = [
            self.transition(
                1,
                1,
                "A",
                2,
                "B",
            ),

            self.transition(
                2,
                2,
                "B",
                1,
                "A",
            ),

            self.transition(
                3,
                2,
                "B",
                3,
                "C",
            ),
        ]


        metadata = {
            3:
                PathTargetMetadata(
                    asset_id=3,
                    asset_name="C",
                    criticality=(
                        "CRITICAL"
                    ),
                )
        }


        result = (
            analyze_attack_paths(
                start_asset_id=1,
                start_asset_name="A",
                start_privilege="LOW",
                transitions=transitions,
                target_metadata=(
                    metadata
                ),
            )
        )


        self.assertEqual(
            result[
                "summary"
            ][
                "attack_paths"
            ],
            1,
        )


    def test_max_depth_is_respected(
        self,
    ):
        transitions = [
            self.transition(
                1,
                1,
                "A",
                2,
                "B",
            ),

            self.transition(
                2,
                2,
                "B",
                3,
                "C",
            ),

            self.transition(
                3,
                3,
                "C",
                4,
                "D",
            ),
        ]


        metadata = {
            4:
                PathTargetMetadata(
                    asset_id=4,
                    asset_name="D",
                    criticality=(
                        "CRITICAL"
                    ),
                )
        }


        result = (
            analyze_attack_paths(
                start_asset_id=1,
                start_asset_name="A",
                start_privilege="LOW",
                transitions=transitions,
                target_metadata=(
                    metadata
                ),
                max_depth=2,
            )
        )


        self.assertEqual(
            result[
                "summary"
            ][
                "attack_paths"
            ],
            0,
        )
