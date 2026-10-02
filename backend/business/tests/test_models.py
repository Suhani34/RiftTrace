from django.core.exceptions import (
    ValidationError,
)
from django.test import TestCase

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


class BusinessModelTests(
    TestCase
):
    def setUp(self):
        self.organization = (
            Organization.objects.create(
                name="BusinessCorp"
            )
        )

        self.other_organization = (
            Organization.objects.create(
                name="OtherBusinessCorp"
            )
        )

        self.asset = Asset.objects.create(
            organization=(
                self.organization
            ),

            name="Checkout API",

            asset_type=(
                Asset.AssetType.API
            ),
        )

        self.other_asset = (
            Asset.objects.create(
                organization=(
                    self.other_organization
                ),

                name="Foreign API",

                asset_type=(
                    Asset.AssetType.API
                ),
            )
        )

        self.process = (
            BusinessProcess.objects.create(
                organization=(
                    self.organization
                ),

                name="Checkout",

                criticality=(
                    BusinessProcess
                    .Criticality
                    .CRITICAL
                ),
            )
        )


    def test_business_process_created(
        self,
    ):
        self.assertEqual(
            self.process.name,
            "Checkout",
        )


    def test_same_organization_dependency(
        self,
    ):
        dependency = (
            BusinessProcessDependency
            .objects
            .create(
                business_process=(
                    self.process
                ),

                asset=self.asset,

                dependency_level=(
                    BusinessProcessDependency
                    .DependencyLevel
                    .ESSENTIAL
                ),
            )
        )

        self.assertEqual(
            dependency.asset,
            self.asset,
        )


    def test_cross_organization_dependency_rejected(
        self,
    ):
        with self.assertRaises(
            ValidationError
        ):
            (
                BusinessProcessDependency
                .objects
                .create(
                    business_process=(
                        self.process
                    ),

                    asset=(
                        self.other_asset
                    ),
                )
            )
