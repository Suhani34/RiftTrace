from django.test import SimpleTestCase

from simulation_engine.identity_propagation import (
    analyze_identity_propagation,
)

from simulation_engine.identity_records import (
    CredentialExposureRecord,
    IdentityAccessRecord,
    IdentityLinkRecord,
    IdentityRecord,
)


class IdentityPropagationEngineTests(
    SimpleTestCase
):
    def test_credential_identity_and_access_expand_assets(
        self,
    ):
        result = analyze_identity_propagation(
            compromised_assets={
                10: "LOW",
            },

            identities=(
                IdentityRecord(
                    id=1,

                    name="web-runtime",

                    identity_type=(
                        "SERVICE_ACCOUNT"
                    ),

                    privilege_level="LOW",

                    enabled=True,
                ),

                IdentityRecord(
                    id=2,

                    name="admin-role",

                    identity_type="ROLE",

                    privilege_level="HIGH",

                    enabled=True,
                ),
            ),

            credentials=(
                CredentialExposureRecord(
                    id=1,

                    name="runtime-token",

                    identity_id=1,

                    stored_on_asset_id=10,

                    credential_type="TOKEN",

                    discoverable_on_compromise=True,

                    satisfies_mfa=False,

                    active=True,
                ),
            ),

            links=(
                IdentityLinkRecord(
                    id=1,

                    source_identity_id=1,

                    target_identity_id=2,

                    link_type=(
                        "ASSUMES_ROLE"
                    ),

                    requires_mfa=False,

                    enabled=True,
                ),
            ),

            accesses=(
                IdentityAccessRecord(
                    id=1,

                    identity_id=2,

                    asset_id=20,

                    access_type=(
                        "ADMINISTER"
                    ),

                    granted_privilege=(
                        "HIGH"
                    ),

                    requires_mfa=False,

                    enabled=True,
                ),
            ),
        )


        self.assertIn(
            (
                20,
                "HIGH",
            ),

            result.compromised_assets,
        )


        self.assertEqual(
            len(
                result.acquired_identities
            ),

            2,
        )


    def test_mfa_blocks_access(
        self,
    ):
        result = analyze_identity_propagation(
            compromised_assets={
                10: "LOW",
            },

            identities=(
                IdentityRecord(
                    id=1,

                    name="user",

                    identity_type="USER",

                    privilege_level="LOW",

                    enabled=True,
                ),
            ),

            credentials=(
                CredentialExposureRecord(
                    id=1,

                    name="password",

                    identity_id=1,

                    stored_on_asset_id=10,

                    credential_type=(
                        "PASSWORD"
                    ),

                    discoverable_on_compromise=True,

                    satisfies_mfa=False,

                    active=True,
                ),
            ),

            links=(),

            accesses=(
                IdentityAccessRecord(
                    id=1,

                    identity_id=1,

                    asset_id=20,

                    access_type="LOGIN",

                    granted_privilege="LOW",

                    requires_mfa=True,

                    enabled=True,
                ),
            ),
        )


        self.assertNotIn(
            (
                20,
                "LOW",
            ),

            result.compromised_assets,
        )


        self.assertEqual(
            len(
                result.blocked_steps
            ),

            1,
        )


        self.assertEqual(
            result
            .blocked_steps[
                0
            ]
            .reason,

            "MFA_REQUIRED",
        )
