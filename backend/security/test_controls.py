from django.core.exceptions import (
    ValidationError,
)

from django.test import TestCase

from assets.models import (
    Asset,
    Relationship,
)

from organizations.models import (
    Organization,
)

from security.models import (
    SecurityControl,
    Vulnerability,
)


class SecurityControlModelTests(
    TestCase
):
    def setUp(self):
        self.organization = (
            Organization.objects.create(
                name="ControlCorp"
            )
        )


        self.other_organization = (
            Organization.objects.create(
                name="OtherControlCorp"
            )
        )


        self.source = (
            Asset.objects.create(
                organization=(
                    self.organization
                ),

                name="Web",

                asset_type=(
                    Asset
                    .AssetType
                    .APPLICATION
                ),
            )
        )


        self.target = (
            Asset.objects.create(
                organization=(
                    self.organization
                ),

                name="API",

                asset_type=(
                    Asset.AssetType.API
                ),
            )
        )


        self.other_asset = (
            Asset.objects.create(
                organization=(
                    self.other_organization
                ),

                name="Foreign",

                asset_type=(
                    Asset.AssetType.API
                ),
            )
        )


        self.relationship = (
            Relationship.objects.create(
                source=self.source,

                target=self.target,

                relationship_type=(
                    Relationship
                    .RelationshipType
                    .CALLS
                ),
            )
        )


        self.vulnerability = (
            Vulnerability.objects.create(
                asset=self.target,

                title="API weakness",

                attack_vector=(
                    Vulnerability
                    .AttackVector
                    .NETWORK
                ),
            )
        )


    def test_segmentation_control_created(
        self,
    ):
        control = (
            SecurityControl.objects.create(
                organization=(
                    self.organization
                ),

                name="Segment path",

                control_type=(
                    SecurityControl
                    .ControlType
                    .NETWORK_SEGMENTATION
                ),

                target_relationship=(
                    self.relationship
                ),
            )
        )


        self.assertEqual(
            control.target_relationship,
            self.relationship,
        )


    def test_remediation_requires_vulnerability(
        self,
    ):
        with self.assertRaises(
            ValidationError
        ):
            SecurityControl.objects.create(
                organization=(
                    self.organization
                ),

                name="Bad remediation",

                control_type=(
                    SecurityControl
                    .ControlType
                    .VULNERABILITY_REMEDIATION
                ),
            )
