from dataclasses import dataclass
from typing import Any


@dataclass(
    frozen=True,
    slots=True,
)
class AttackMappingRuleRecord:
    rule_code: str

    event_type: str

    technique_attack_id: str

    conditions: tuple[
        tuple[str, Any],
        ...,
    ]

    priority: int

    enabled: bool


@dataclass(
    frozen=True,
    slots=True,
)
class AttackMappingMatch:
    rule_code: str

    technique_attack_id: str


def _conditions_match(
    *,
    conditions,
    attributes,
):
    for (
        field_name,
        expected_value,
    ) in conditions:
        actual_value = (
            attributes.get(
                field_name
            )
        )


        if (
            actual_value
            != expected_value
        ):
            return False


    return True


def evaluate_attack_mapping(
    *,
    event_type,
    attributes,
    rules,
):
    """
    Evaluate a normalized RiftTrace event
    against deterministic ATT&CK rules.

    This function does not claim that an
    ATT&CK technique actually occurred.

    It only returns techniques whose rule
    conditions are consistent with the
    modeled event.
    """

    matches = []


    ordered_rules = sorted(
        rules,

        key=lambda rule: (
            rule.priority,
            rule.rule_code,
        ),
    )


    for rule in ordered_rules:
        if not rule.enabled:
            continue


        if (
            rule.event_type
            != event_type
        ):
            continue


        if not _conditions_match(
            conditions=rule.conditions,

            attributes=attributes,
        ):
            continue


        matches.append(
            AttackMappingMatch(
                rule_code=(
                    rule.rule_code
                ),

                technique_attack_id=(
                    rule
                    .technique_attack_id
                ),
            )
        )


    return tuple(
        matches
    )
