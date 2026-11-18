from django.core.exceptions import (
    ValidationError,
)

from django.test import (
    TestCase,
)

from assets.models import (
    Asset,
)

from business.models import (
    BusinessProcess,
    BusinessProcessDependency,
)

from organizations.models import (
    Organization,
)


class BusinessIntegrityTests(
    TestCase
):
    def setUp(self):
        self.organization_a = (
            Organization.objects.create(
                name="Business Org A"
            )
        )

        self.organization_b = (
            Organization.objects.create(
                name="Business Org B"
            )
        )


        self.process = (
            BusinessProcess.objects.create(
                organization=(
                    self.organization_a
                ),

                name=(
                    "Order Processing"
                ),

                criticality=(
                    BusinessProcess
                    .Criticality
                    .CRITICAL
                ),
            )
        )


        self.asset_a = (
            Asset.objects.create(
                organization=(
                    self.organization_a
                ),

                name=(
                    "Order API"
                ),

                asset_type=(
                    Asset
                    .AssetType
                    .API
                ),
            )
        )


        self.asset_b = (
            Asset.objects.create(
                organization=(
                    self.organization_b
                ),

                name=(
                    "Foreign Database"
                ),

                asset_type=(
                    Asset
                    .AssetType
                    .DATABASE
                ),
            )
        )


    def test_same_organization_dependency_is_valid(
        self,
    ):
        dependency = (
            BusinessProcessDependency(
                business_process=(
                    self.process
                ),

                asset=(
                    self.asset_a
                ),

                dependency_level=(
                    BusinessProcessDependency
                    .DependencyLevel
                    .ESSENTIAL
                ),
            )
        )


        dependency.full_clean()


    def test_cross_organization_dependency_is_rejected(
        self,
    ):
        dependency = (
            BusinessProcessDependency(
                business_process=(
                    self.process
                ),

                asset=(
                    self.asset_b
                ),

                dependency_level=(
                    BusinessProcessDependency
                    .DependencyLevel
                    .ESSENTIAL
                ),
            )
        )


        with self.assertRaises(
            ValidationError
        ):
            dependency.full_clean()
