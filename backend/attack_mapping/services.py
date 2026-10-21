from simulation_engine.attack_mapping import (
    AttackMappingRuleRecord,
    evaluate_attack_mapping,
)

from .models import (
    AttackMappingRule,
    AttackTechnique,
)


def load_attack_mapping_context():
    technique_objects = {
        item.attack_id:
            item

        for item
        in AttackTechnique.objects.filter(
            enabled=True
        )
    }


    rule_objects = (
        AttackMappingRule
        .objects
        .filter(
            enabled=True,

            technique__enabled=True,
        )
        .select_related(
            "technique"
        )
        .order_by(
            "priority",
            "rule_code",
        )
    )


    rule_records = tuple(
        AttackMappingRuleRecord(
            rule_code=(
                item.rule_code
            ),

            event_type=(
                item.event_type
            ),

            technique_attack_id=(
                item
                .technique
                .attack_id
            ),

            conditions=tuple(
                item.conditions.items()
            ),

            priority=(
                item.priority
            ),

            enabled=(
                item.enabled
            ),
        )

        for item
        in rule_objects
    )


    rule_objects_by_code = {
        item.rule_code:
            item

        for item
        in rule_objects
    }


    return {
        "techniques":
            technique_objects,

        "rules":
            rule_records,

        "rule_objects":
            rule_objects_by_code,
    }


def map_attack_event(
    *,
    event_type,
    attributes,
    context=None,
):
    if context is None:
        context = (
            load_attack_mapping_context()
        )


    matches = (
        evaluate_attack_mapping(
            event_type=event_type,

            attributes=attributes,

            rules=context[
                "rules"
            ],
        )
    )


    annotations = []

    seen_techniques = set()


    for match in matches:
        attack_id = (
            match
            .technique_attack_id
        )


        if (
            attack_id
            in seen_techniques
        ):
            continue


        technique = (
            context[
                "techniques"
            ].get(
                attack_id
            )
        )


        rule = (
            context[
                "rule_objects"
            ].get(
                match.rule_code
            )
        )


        if (
            technique is None
            or rule is None
        ):
            continue


        seen_techniques.add(
            attack_id
        )


        annotations.append(
            {
                "attack_id":
                    technique.attack_id,

                "name":
                    technique.name,

                "tactics":
                    technique.tactics,

                "source_version":
                    (
                        technique
                        .source_version
                    ),

                "source_url":
                    technique.source_url,

                "rule_code":
                    rule.rule_code,

                "basis":
                    rule.rationale,
            }
        )


    return annotations
