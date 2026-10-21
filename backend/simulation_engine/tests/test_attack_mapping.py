from django.test import SimpleTestCase

from simulation_engine.attack_mapping import (
    AttackMappingRuleRecord,
    evaluate_attack_mapping,
)


class AttackMappingEngineTests(
    SimpleTestCase
):
    def setUp(self):
        self.rules = (
            AttackMappingRuleRecord(
                rule_code=(
                    "CREDENTIAL"
                ),

                event_type=(
                    "CREDENTIAL_DISCOVERY"
                ),

                technique_attack_id=(
                    "T1552"
                ),

                conditions=(),

                priority=10,

                enabled=True,
            ),

            AttackMappingRuleRecord(
                rule_code=(
                    "VALID_ACCOUNT"
                ),

                event_type=(
                    "IDENTITY_ACCESS"
                ),

                technique_attack_id=(
                    "T1078"
                ),

                conditions=(),

                priority=20,

                enabled=True,
            ),

            AttackMappingRuleRecord(
                rule_code=(
                    "REMOTE_SERVICE"
                ),

                event_type=(
                    "IDENTITY_ACCESS"
                ),

                technique_attack_id=(
                    "T1021"
                ),

                conditions=(
                    (
                        "access_type",
                        "REMOTE_SERVICE",
                    ),
                ),

                priority=30,

                enabled=True,
            ),

            AttackMappingRuleRecord(
                rule_code=(
                    "PUBLIC_EXPLOIT"
                ),

                event_type=(
                    "VULNERABILITY_EXPLOIT"
                ),

                technique_attack_id=(
                    "T1190"
                ),

                conditions=(
                    (
                        "internet_exposed",
                        True,
                    ),
                ),

                priority=40,

                enabled=True,
            ),
        )


    def test_credential_discovery_maps_to_t1552(
        self,
    ):
        result = (
            evaluate_attack_mapping(
                event_type=(
                    "CREDENTIAL_DISCOVERY"
                ),

                attributes={
                    "credential_type":
                        "TOKEN"
                },

                rules=self.rules,
            )
        )


        self.assertEqual(
            [
                item.technique_attack_id

                for item
                in result
            ],

            [
                "T1552",
            ],
        )


    def test_remote_identity_access_maps_to_two_techniques(
        self,
    ):
        result = (
            evaluate_attack_mapping(
                event_type=(
                    "IDENTITY_ACCESS"
                ),

                attributes={
                    "access_type":
                        "REMOTE_SERVICE"
                },

                rules=self.rules,
            )
        )


        technique_ids = {
            item.technique_attack_id

            for item
            in result
        }


        self.assertEqual(
            technique_ids,

            {
                "T1078",
                "T1021",
            },
        )


    def test_non_remote_access_does_not_map_to_remote_services(
        self,
    ):
        result = (
            evaluate_attack_mapping(
                event_type=(
                    "IDENTITY_ACCESS"
                ),

                attributes={
                    "access_type":
                        "ADMINISTER"
                },

                rules=self.rules,
            )
        )


        technique_ids = {
            item.technique_attack_id

            for item
            in result
        }


        self.assertIn(
            "T1078",
            technique_ids,
        )


        self.assertNotIn(
            "T1021",
            technique_ids,
        )


    def test_public_exploit_requires_internet_exposure(
        self,
    ):
        exposed = (
            evaluate_attack_mapping(
                event_type=(
                    "VULNERABILITY_EXPLOIT"
                ),

                attributes={
                    "internet_exposed":
                        True
                },

                rules=self.rules,
            )
        )


        internal = (
            evaluate_attack_mapping(
                event_type=(
                    "VULNERABILITY_EXPLOIT"
                ),

                attributes={
                    "internet_exposed":
                        False
                },

                rules=self.rules,
            )
        )


        self.assertEqual(
            [
                item.technique_attack_id

                for item
                in exposed
            ],

            [
                "T1190",
            ],
        )


        self.assertEqual(
            internal,
            (),
        )
