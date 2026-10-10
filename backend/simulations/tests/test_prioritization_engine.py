from django.test import SimpleTestCase

from simulation_engine.business_records import (
    BusinessDependencyRecord,
    BusinessProcessRecord,
)

from simulation_engine.control_records import (
    SecurityControlRecord,
)

from simulation_engine.graph_builder import (
    build_topology_graph,
)

from simulation_engine.prioritization import (
    rank_security_controls,
)

from simulation_engine.records import (
    AssetRecord,
    RelationshipRecord,
    VulnerabilityRecord,
)


class PrioritizationEngineTests(
    SimpleTestCase
):
    def setUp(self):
        self.assets = [
            AssetRecord(
                id=1,
                name="Web",
                asset_type="APPLICATION",
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
        ]


        self.relationships = [
            RelationshipRecord(
                id=101,
                source_id=1,
                target_id=2,
                relationship_type="CALLS",
                protocol="HTTPS",
                port=443,
                requires_authentication=False,
                required_source_privilege="LOW",
            ),

            RelationshipRecord(
                id=102,
                source_id=2,
                target_id=3,
                relationship_type="READS",
                protocol="TCP",
                port=5432,
                requires_authentication=False,
                required_source_privilege="LOW",
            ),
        ]


        self.vulnerabilities = (
            VulnerabilityRecord(
                id=201,
                asset_id=2,
                title="API weakness",
                reference_id="TEST-API",
                attack_vector="NETWORK",
                privileges_required="NONE",
                grants_privilege="LOW",
                bypasses_authentication=True,
                is_exploitable=True,
                bypasses_mfa=False,
            ),

            VulnerabilityRecord(
                id=202,
                asset_id=3,
                title="Database weakness",
                reference_id="TEST-DB",
                attack_vector="NETWORK",
                privileges_required="NONE",
                grants_privilege="LOW",
                bypasses_authentication=True,
                is_exploitable=True,
                bypasses_mfa=False,
            ),
        )


        self.processes = (
            BusinessProcessRecord(
                id=301,
                name="Checkout",
                criticality="CRITICAL",
                impact_description=(
                    "Checkout may be affected."
                ),
            ),
        )


        self.dependencies = (
            BusinessDependencyRecord(
                id=401,
                business_process_id=301,
                asset_id=3,
                dependency_level="ESSENTIAL",
            ),
        )


        self.controls = (
            SecurityControlRecord(
                id=501,

                name="Segment Web API",

                control_type=(
                    "NETWORK_SEGMENTATION"
                ),

                target_relationship_id=101,

                target_vulnerability_id=None,
            ),

            SecurityControlRecord(
                id=502,

                name="Patch API",

                control_type=(
                    "VULNERABILITY_REMEDIATION"
                ),

                target_relationship_id=None,

                target_vulnerability_id=201,
            ),

            SecurityControlRecord(
                id=503,

                name="Segment API Database",

                control_type=(
                    "NETWORK_SEGMENTATION"
                ),

                target_relationship_id=102,

                target_vulnerability_id=None,
            ),

            SecurityControlRecord(
                id=504,

                name="Require Auth Web API",

                control_type=(
                    "AUTHENTICATION_ENFORCEMENT"
                ),

                target_relationship_id=101,

                target_vulnerability_id=None,
            ),
        )


        self.graph = (
            build_topology_graph(
                self.assets,
                self.relationships,
            )
        )


    def run_ranking(self):
        return rank_security_controls(
            graph=self.graph,

            vulnerabilities=(
                self.vulnerabilities
            ),

            business_processes=(
                self.processes
            ),

            dependencies=(
                self.dependencies
            ),

            controls=(
                self.controls
            ),

            start_asset_id=1,

            start_privilege="LOW",
        )


    def test_upstream_controls_rank_above_downstream_control(
        self,
    ):
        result = self.run_ranking()


        by_id = {
            ranked.control_id:
                ranked

            for ranked
            in result.ranked_controls
        }


        self.assertLess(
            by_id[501].priority_rank,

            by_id[503].priority_rank,
        )


    def test_equal_effect_controls_share_rank(
        self,
    ):
        result = self.run_ranking()


        by_id = {
            ranked.control_id:
                ranked

            for ranked
            in result.ranked_controls
        }


        self.assertEqual(
            by_id[501].priority_rank,

            by_id[502].priority_rank,
        )


    def test_zero_effect_control_ranks_lower(
        self,
    ):
        result = self.run_ranking()


        by_id = {
            ranked.control_id:
                ranked

            for ranked
            in result.ranked_controls
        }


        self.assertFalse(
            by_id[
                504
            ].has_measured_effect
        )


        self.assertGreater(
            by_id[
                504
            ].priority_rank,

            by_id[
                501
            ].priority_rank,
        )


    def test_database_control_prevents_critical_asset(
        self,
    ):
        result = self.run_ranking()


        by_id = {
            ranked.control_id:
                ranked

            for ranked
            in result.ranked_controls
        }


        self.assertEqual(
            by_id[
                503
            ].metrics
            .critical_asset_reduction,

            1,
        )


    def test_ranking_contains_all_controls(
        self,
    ):
        result = self.run_ranking()


        self.assertEqual(
            len(
                result.ranked_controls
            ),

            4,
        )
