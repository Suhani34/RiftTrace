from django.test import SimpleTestCase

from simulation_engine.business_records import (
    BusinessDependencyRecord,
    BusinessProcessRecord,
)

from simulation_engine.counterfactual import (
    analyze_counterfactual,
)

from simulation_engine.graph_builder import (
    build_topology_graph,
)

from simulation_engine.records import (
    AssetRecord,
    RelationshipRecord,
    VulnerabilityRecord,
)


class CounterfactualEngineTests(
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
        ]


        self.vulnerabilities = (
            VulnerabilityRecord(
                id=201,
                asset_id=2,
                title="API weakness",
                reference_id="TEST-201",
                attack_vector="NETWORK",
                privileges_required="NONE",
                grants_privilege="LOW",
                bypasses_authentication=True,
                is_exploitable=True,
            ),

            VulnerabilityRecord(
                id=202,
                asset_id=3,
                title="Database weakness",
                reference_id="TEST-202",
                attack_vector="NETWORK",
                privileges_required="NONE",
                grants_privilege="LOW",
                bypasses_authentication=True,
                is_exploitable=True,
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


        self.graph = (
            build_topology_graph(
                self.assets,
                self.relationships,
            )
        )


    def test_disabling_relationship_reduces_propagation(
        self,
    ):
        result = analyze_counterfactual(
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

            start_asset_id=1,

            start_privilege="LOW",

            disabled_relationship_ids=(
                101,
            ),
        )


        self.assertEqual(
            result
            .propagated_asset_reduction,
            2,
        )


        self.assertEqual(
            set(
                result
                .prevented_propagated_asset_ids
            ),
            {2, 3},
        )


    def test_disabling_vulnerability_reduces_propagation(
        self,
    ):
        result = analyze_counterfactual(
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

            start_asset_id=1,

            start_privilege="LOW",

            disabled_vulnerability_ids=(
                201,
            ),
        )


        self.assertEqual(
            set(
                result
                .prevented_propagated_asset_ids
            ),
            {2, 3},
        )


    def test_business_process_can_be_avoided(
        self,
    ):
        result = analyze_counterfactual(
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

            start_asset_id=1,

            start_privilege="LOW",

            disabled_relationship_ids=(
                101,
            ),
        )


        self.assertEqual(
            result
            .avoided_business_process_ids,
            (301,),
        )


    def test_original_graph_is_unchanged(
        self,
    ):
        analyze_counterfactual(
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

            start_asset_id=1,

            start_privilege="LOW",

            disabled_relationship_ids=(
                101,
            ),
        )


        self.assertTrue(
            self.graph.has_edge(
                1,
                2,
                key=101,
            )
        )


    def test_original_vulnerability_tuple_is_unchanged(
        self,
    ):
        analyze_counterfactual(
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

            start_asset_id=1,

            start_privilege="LOW",

            disabled_vulnerability_ids=(
                201,
            ),
        )


        self.assertEqual(
            len(
                self.vulnerabilities
            ),
            2,
        )
