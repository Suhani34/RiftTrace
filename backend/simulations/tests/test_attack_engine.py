from django.test import SimpleTestCase

from simulation_engine.attack_propagation import (
    analyze_attack_propagation,
)

from simulation_engine.graph_builder import (
    build_topology_graph,
)

from simulation_engine.records import (
    AssetRecord,
    RelationshipRecord,
    VulnerabilityRecord,
)


class AttackPropagationEngineTests(
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
                name="Admin",
                asset_type="WORKSTATION",
                criticality="HIGH",
                environment="PRODUCTION",
                network_zone_id=2,
                is_internet_exposed=False,
            ),

            AssetRecord(
                id=4,
                name="Domain Controller",
                asset_type="DOMAIN_CONTROLLER",
                criticality="CRITICAL",
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
                relationship_type="CONNECTS_TO",
                protocol="HTTPS",
                port=443,
                requires_authentication=False,
                required_source_privilege="HIGH",
            ),

            RelationshipRecord(
                id=103,
                source_id=3,
                target_id=4,
                relationship_type="AUTHENTICATES_TO",
                protocol="TCP",
                port=445,
                requires_authentication=True,
                required_source_privilege="LOW",
            ),
        ]

        self.vulnerabilities = (
            VulnerabilityRecord(
                id=201,
                asset_id=2,
                title="API remote weakness",
                reference_id="DEMO-201",
                attack_vector="NETWORK",
                privileges_required="NONE",
                grants_privilege="LOW",
                bypasses_authentication=True,
                is_exploitable=True,
            ),

            VulnerabilityRecord(
                id=202,
                asset_id=2,
                title="API local escalation",
                reference_id="DEMO-202",
                attack_vector="LOCAL",
                privileges_required="LOW",
                grants_privilege="HIGH",
                bypasses_authentication=False,
                is_exploitable=True,
            ),

            VulnerabilityRecord(
                id=203,
                asset_id=3,
                title="Admin remote weakness",
                reference_id="DEMO-203",
                attack_vector="NETWORK",
                privileges_required="NONE",
                grants_privilege="LOW",
                bypasses_authentication=False,
                is_exploitable=True,
            ),

            VulnerabilityRecord(
                id=204,
                asset_id=4,
                title="DC weakness",
                reference_id="DEMO-204",
                attack_vector="NETWORK",
                privileges_required="NONE",
                grants_privilege="HIGH",
                bypasses_authentication=False,
                is_exploitable=True,
            ),
        )

        self.graph = (
            build_topology_graph(
                self.assets,
                self.relationships,
            )
        )

    def test_remote_vulnerability_allows_propagation(
        self,
    ):
        result = (
            analyze_attack_propagation(
                self.graph,
                self.vulnerabilities,
                start_asset_id=1,
                start_privilege="LOW",
            )
        )

        ids = {
            item.asset_id
            for item
            in result.propagated_assets
        }

        self.assertIn(
            2,
            ids,
        )

    def test_local_escalation_unlocks_relationship(
        self,
    ):
        result = (
            analyze_attack_propagation(
                self.graph,
                self.vulnerabilities,
                start_asset_id=1,
                start_privilege="LOW",
            )
        )

        ids = {
            item.asset_id
            for item
            in result.propagated_assets
        }

        self.assertIn(
            3,
            ids,
        )

        api = next(
            item
            for item
            in result.propagated_assets
            if item.asset_id == 2
        )

        self.assertEqual(
            api.privilege,
            "HIGH",
        )

    def test_authentication_can_block_transition(
        self,
    ):
        result = (
            analyze_attack_propagation(
                self.graph,
                self.vulnerabilities,
                start_asset_id=1,
                start_privilege="LOW",
            )
        )

        ids = {
            item.asset_id
            for item
            in result.propagated_assets
        }

        self.assertNotIn(
            4,
            ids,
        )

        codes = {
            blocked.reason_code

            for blocked
            in result.blocked_transitions
        }

        self.assertIn(
            "AUTHENTICATION_REQUIRED",
            codes,
        )
