from django.core.management.base import (
    BaseCommand,
)

from attack_mapping.models import (
    AttackMappingRule,
    AttackTechnique,
)


ATTACK_VERSION = "20.0"


TECHNIQUES = [
    {
        "attack_id": "T1190",

        "name": (
            "Exploit Public-Facing "
            "Application"
        ),

        "tactics": [
            "Initial Access",
        ],

        "source_url": (
            "https://attack.mitre.org/"
            "techniques/T1190/"
        ),
    },

    {
        "attack_id": "T1552",

        "name": (
            "Unsecured Credentials"
        ),

        "tactics": [
            "Credential Access",
        ],

        "source_url": (
            "https://attack.mitre.org/"
            "techniques/T1552/"
        ),
    },

    {
        "attack_id": "T1078",

        "name": (
            "Valid Accounts"
        ),

        "tactics": [
            "Initial Access",
            "Persistence",
            "Privilege Escalation",
            "Stealth",
        ],

        "source_url": (
            "https://attack.mitre.org/"
            "techniques/T1078/"
        ),
    },

    {
        "attack_id": "T1021",

        "name": (
            "Remote Services"
        ),

        "tactics": [
            "Lateral Movement",
        ],

        "source_url": (
            "https://attack.mitre.org/"
            "techniques/T1021/"
        ),
    },
]


RULES = [
    {
        "rule_code":
            "PUBLIC_FACING_EXPLOIT",

        "name":
            (
                "Public-facing "
                "vulnerability exploitation"
            ),

        "event_type":
            (
                AttackMappingRule
                .EventType
                .VULNERABILITY_EXPLOIT
            ),

        "technique_attack_id":
            "T1190",

        "conditions": {
            "internet_exposed":
                True,
        },

        "rationale":
            (
                "The modeled event "
                "represents exploitation "
                "of an Internet-exposed "
                "vulnerable application."
            ),

        "priority":
            10,
    },

    {
        "rule_code":
            "EXPOSED_CREDENTIAL_DISCOVERY",

        "name":
            (
                "Credential discovery "
                "on compromised asset"
            ),

        "event_type":
            (
                AttackMappingRule
                .EventType
                .CREDENTIAL_DISCOVERY
            ),

        "technique_attack_id":
            "T1552",

        "conditions": {},

        "rationale":
            (
                "The modeled event "
                "represents a credential "
                "becoming available from "
                "a compromised asset."
            ),

        "priority":
            20,
    },

    {
        "rule_code":
            "VALID_ACCOUNT_ACCESS",

        "name":
            (
                "Use of modeled identity "
                "for asset access"
            ),

        "event_type":
            (
                AttackMappingRule
                .EventType
                .IDENTITY_ACCESS
            ),

        "technique_attack_id":
            "T1078",

        "conditions": {},

        "rationale":
            (
                "The modeled event uses "
                "an acquired identity or "
                "account to access another "
                "resource."
            ),

        "priority":
            30,
    },

    {
        "rule_code":
            "REMOTE_SERVICE_ACCESS",

        "name":
            (
                "Identity access through "
                "remote service"
            ),

        "event_type":
            (
                AttackMappingRule
                .EventType
                .IDENTITY_ACCESS
            ),

        "technique_attack_id":
            "T1021",

        "conditions": {
            "access_type":
                "REMOTE_SERVICE",
        },

        "rationale":
            (
                "The modeled identity "
                "access occurs through a "
                "remote service."
            ),

        "priority":
            40,
    },
]


class Command(BaseCommand):
    help = (
        "Seed RiftTrace's curated "
        "MITRE ATT&CK v20 mapping catalog."
    )


    def handle(
        self,
        *args,
        **options,
    ):
        techniques_by_attack_id = {}


        for item in TECHNIQUES:
            technique, _ = (
                AttackTechnique
                .objects
                .update_or_create(
                    attack_id=(
                        item[
                            "attack_id"
                        ]
                    ),

                    defaults={
                        "name":
                            item[
                                "name"
                            ],

                        "domain":
                            (
                                AttackTechnique
                                .Domain
                                .ENTERPRISE
                            ),

                        "tactics":
                            item[
                                "tactics"
                            ],

                        "is_subtechnique":
                            False,

                        "parent_attack_id":
                            "",

                        "source_version":
                            ATTACK_VERSION,

                        "source_url":
                            item[
                                "source_url"
                            ],

                        "enabled":
                            True,
                    },
                )
            )


            techniques_by_attack_id[
                technique.attack_id
            ] = technique


        for item in RULES:
            technique = (
                techniques_by_attack_id[
                    item[
                        "technique_attack_id"
                    ]
                ]
            )


            AttackMappingRule.objects.update_or_create(
                rule_code=(
                    item[
                        "rule_code"
                    ]
                ),

                defaults={
                    "name":
                        item[
                            "name"
                        ],

                    "event_type":
                        item[
                            "event_type"
                        ],

                    "technique":
                        technique,

                    "conditions":
                        item[
                            "conditions"
                        ],

                    "rationale":
                        item[
                            "rationale"
                        ],

                    "priority":
                        item[
                            "priority"
                        ],

                    "enabled":
                        True,
                },
            )


        self.stdout.write(
            self.style.SUCCESS(
                (
                    "MITRE ATT&CK v20 "
                    "catalog and mapping "
                    "rules seeded."
                )
            )
        )
