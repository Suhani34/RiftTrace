from django.test import SimpleTestCase

from simulation_engine.business_impact import (
    analyze_business_impact,
)

from simulation_engine.business_records import (
    BusinessDependencyRecord,
    BusinessProcessRecord,
)


class BusinessImpactEngineTests(
    SimpleTestCase
):
    def setUp(self):
        self.processes = (
            BusinessProcessRecord(
                id=1,
                name="Checkout",
                criticality="CRITICAL",
                impact_description=(
                    "Checkout may be affected."
                ),
            ),

            BusinessProcessRecord(
                id=2,
                name="Deployment",
                criticality="HIGH",
                impact_description=(
                    "Deployments may be affected."
                ),
            ),
        )


        self.dependencies = (
            BusinessDependencyRecord(
                id=101,

                business_process_id=1,

                asset_id=10,

                dependency_level=(
                    "ESSENTIAL"
                ),
            ),

            BusinessDependencyRecord(
                id=102,

                business_process_id=1,

                asset_id=11,

                dependency_level=(
                    "IMPORTANT"
                ),
            ),

            BusinessDependencyRecord(
                id=103,

                business_process_id=2,

                asset_id=20,

                dependency_level=(
                    "ESSENTIAL"
                ),
            ),
        )


    def test_process_becomes_impacted(
        self,
    ):
        result = (
            analyze_business_impact(
                self.processes,
                self.dependencies,
                {10},
            )
        )

        self.assertEqual(
            result
            .impacted_process_count,
            1,
        )

        self.assertEqual(
            result
            .impacted_processes[0]
            .business_process_id,
            1,
        )


    def test_unrelated_process_not_impacted(
        self,
    ):
        result = (
            analyze_business_impact(
                self.processes,
                self.dependencies,
                {10},
            )
        )

        ids = {
            item.business_process_id

            for item
            in result.impacted_processes
        }

        self.assertNotIn(
            2,
            ids,
        )


    def test_strongest_dependency_selected(
        self,
    ):
        result = (
            analyze_business_impact(
                self.processes,
                self.dependencies,
                {10, 11},
            )
        )

        impact = (
            result
            .impacted_processes[0]
        )

        self.assertEqual(
            impact
            .strongest_dependency_level,
            "ESSENTIAL",
        )


    def test_critical_process_count(
        self,
    ):
        result = (
            analyze_business_impact(
                self.processes,
                self.dependencies,
                {10},
            )
        )

        self.assertEqual(
            result
            .critical_process_count,
            1,
        )


    def test_no_affected_assets_returns_zero(
        self,
    ):
        result = (
            analyze_business_impact(
                self.processes,
                self.dependencies,
                set(),
            )
        )

        self.assertEqual(
            result
            .impacted_process_count,
            0,
        )
