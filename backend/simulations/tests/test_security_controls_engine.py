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

from simulation_engine.records import (
    AssetRecord,
    RelationshipRecord,
    VulnerabilityRecord,
)

from simulation_engine.security_controls import (
    analyze_security_controls,
)


class SecurityControlEngineTests(
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
                requires_authentication=False,
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
                bypasses_authentication=False,
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
                asset_id=2,
                dependency_level="ESSENTIAL",
            ),
        )


        self.graph = (
            build_topology_graph(
                self.assets,
                self.relationships,
            )
        )


    def run_control(
        self,
        control,
    ):
        return analyze_security_controls(
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

            controls=(control,),

            start_asset_id=1,

            start_privilege="LOW",
        )


    def test_network_segmentation_blocks_path(
        self,
    ):
        result = self.run_control(
            SecurityControlRecord(
                id=501,

                name="Segment",

                control_type=(
                    "NETWORK_SEGMENTATION"
                ),

                target_relationship_id=101,

                target_vulnerability_id=None,
            )
        )


        self.assertEqual(
            result
            .comparison
            .propagated_asset_reduction,
            1,
        )


    def test_vulnerability_remediation_blocks_path(
        self,
    ):
        result = self.run_control(
            SecurityControlRecord(
                id=502,

                name="Patch",

                control_type=(
                    "VULNERABILITY_REMEDIATION"
                ),

                target_relationship_id=None,

                target_vulnerability_id=201,
            )
        )


        self.assertEqual(
            result
            .comparison
            .propagated_asset_reduction,
            1,
        )


    def test_authentication_enforcement_blocks_non_bypass_vulnerability(
        self,
    ):
        result = self.run_control(
            SecurityControlRecord(
                id=503,

                name="Require auth",

                control_type=(
                    "AUTHENTICATION_ENFORCEMENT"
                ),

                target_relationship_id=101,

                target_vulnerability_id=None,
            )
        )


        self.assertEqual(
            result
            .comparison
            .propagated_asset_reduction,
            1,
        )


    def test_mfa_blocks_non_mfa_bypass_vulnerability(
        self,
    ):
        vulnerable = (
            VulnerabilityRecord(
                id=202,

                asset_id=2,

                title="Auth bypass",

                reference_id="TEST-202",

                attack_vector="NETWORK",

                privileges_required="NONE",

                grants_privilege="LOW",

                bypasses_authentication=True,

                is_exploitable=True,

                bypasses_mfa=False,
            ),
        )


        result = analyze_security_controls(
            graph=self.graph,

            vulnerabilities=vulnerable,

            business_processes=(
                self.processes
            ),

            dependencies=(
                self.dependencies
            ),

            controls=(
                SecurityControlRecord(
                    id=504,

                    name="Require MFA",

                    control_type="MFA",

                    target_relationship_id=101,

                    target_vulnerability_id=None,
                ),
            ),

            start_asset_id=1,

            start_privilege="LOW",
        )


        self.assertEqual(
            result
            .comparison
            .propagated_asset_reduction,
            1,
        )


    def test_least_privilege_blocks_low_privilege_source(
        self,
    ):
        result = self.run_control(
            SecurityControlRecord(
                id=505,

                name="Least privilege",

                control_type=(
                    "LEAST_PRIVILEGE"
                ),

                target_relationship_id=101,

                target_vulnerability_id=None,
            )
        )


        self.assertEqual(
            result
            .comparison
            .propagated_asset_reduction,
            1,
        )
