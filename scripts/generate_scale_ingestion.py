import argparse
import copy
import json
import math

from pathlib import Path


def replace_strings(
    value,
    mapping,
):
    if isinstance(
        value,
        str,
    ):
        return mapping.get(
            value,
            value,
        )


    if isinstance(
        value,
        list,
    ):
        return [
            replace_strings(
                item,
                mapping,
            )

            for item
            in value
        ]


    if isinstance(
        value,
        dict,
    ):
        return {
            key:
                replace_strings(
                    item,
                    mapping,
                )

            for key, item
            in value.items()
        }


    return value


def find_asset_references(
    value,
    asset_names,
):
    references = set()


    if isinstance(
        value,
        str,
    ):
        if value in asset_names:
            references.add(
                value
            )


    elif isinstance(
        value,
        list,
    ):
        for item in value:
            references.update(
                find_asset_references(
                    item,
                    asset_names,
                )
            )


    elif isinstance(
        value,
        dict,
    ):
        for item in value.values():
            references.update(
                find_asset_references(
                    item,
                    asset_names,
                )
            )


    return references


def relationship_endpoint_keys(
    relationship,
    asset_names,
):
    candidates = [
        key

        for key, value
        in relationship.items()

        if (
            isinstance(
                value,
                str,
            )
            and value
            in asset_names
        )
    ]


    if len(
        candidates
    ) < 2:
        raise ValueError(
            (
                "Could not detect two "
                "asset-reference fields "
                "inside the relationship "
                "template."
            )
        )


    source_key = next(
        (
            key

            for key
            in candidates

            if (
                "source"
                in key.lower()
                or "from"
                in key.lower()
            )
        ),

        candidates[0],
    )


    remaining = [
        key

        for key
        in candidates

        if key != source_key
    ]


    target_key = next(
        (
            key

            for key
            in remaining

            if (
                "target"
                in key.lower()
                or "to"
                in key.lower()
            )
        ),

        remaining[0],
    )


    return (
        source_key,
        target_key,
    )


def prefixed_name(
    copy_number,
    original_name,
):
    return (
        f"scale-{copy_number:05d}-"
        f"{original_name}"
    )


def build_scaled_environment(
    template,
    target_assets,
):
    template_assets = (
        template.get(
            "assets",
            []
        )
    )

    template_relationships = (
        template.get(
            "relationships",
            []
        )
    )

    template_vulnerabilities = (
        template.get(
            "vulnerabilities",
            []
        )
    )


    if not template_assets:
        raise ValueError(
            (
                "Template contains "
                "no assets."
            )
        )


    if not template_relationships:
        raise ValueError(
            (
                "Template contains "
                "no relationships."
            )
        )


    original_asset_names = {
        asset[
            "name"
        ]

        for asset
        in template_assets
    }


    relationship_template = (
        template_relationships[
            0
        ]
    )


    (
        source_key,
        target_key,
    ) = relationship_endpoint_keys(
        relationship_template,
        original_asset_names,
    )


    output = copy.deepcopy(
        template
    )


    output[
        "network_zones"
    ] = copy.deepcopy(
        template.get(
            "network_zones",
            []
        )
    )

    output[
        "assets"
    ] = []

    output[
        "relationships"
    ] = []

    output[
        "vulnerabilities"
    ] = []


    assets_per_copy = len(
        template_assets
    )


    copy_count = math.ceil(
        target_assets
        / assets_per_copy
    )


    previous_last_asset = None

    generated_count = 0


    for copy_number in range(
        1,
        copy_count + 1,
    ):
        remaining = (
            target_assets
            - generated_count
        )


        included_assets = (
            template_assets[
                :min(
                    remaining,
                    assets_per_copy,
                )
            ]
        )


        asset_mapping = {
            asset[
                "name"
            ]:
                prefixed_name(
                    copy_number,
                    asset[
                        "name"
                    ],
                )

            for asset
            in included_assets
        }


        general_mapping = dict(
            asset_mapping
        )


        for collection_name in (
            "relationships",
            "vulnerabilities",
        ):
            for item in template.get(
                collection_name,
                []
            ):
                item_name = (
                    item.get(
                        "name"
                    )
                )


                if item_name:
                    general_mapping[
                        item_name
                    ] = (
                        prefixed_name(
                            copy_number,
                            item_name,
                        )
                    )


        cloned_assets = [
            replace_strings(
                copy.deepcopy(
                    asset
                ),
                general_mapping,
            )

            for asset
            in included_assets
        ]


        output[
            "assets"
        ].extend(
            cloned_assets
        )


        current_asset_names = set(
            asset_mapping.values()
        )


        for relationship in (
            template_relationships
        ):
            original_refs = (
                find_asset_references(
                    relationship,
                    original_asset_names,
                )
            )


            if not (
                original_refs
                <= set(
                    asset_mapping.keys()
                )
            ):
                continue


            cloned_relationship = (
                replace_strings(
                    copy.deepcopy(
                        relationship
                    ),
                    general_mapping,
                )
            )


            output[
                "relationships"
            ].append(
                cloned_relationship
            )


        for vulnerability in (
            template_vulnerabilities
        ):
            original_refs = (
                find_asset_references(
                    vulnerability,
                    original_asset_names,
                )
            )


            if (
                original_refs
                and not (
                    original_refs
                    <= set(
                        asset_mapping.keys()
                    )
                )
            ):
                continue


            cloned_vulnerability = (
                replace_strings(
                    copy.deepcopy(
                        vulnerability
                    ),
                    general_mapping,
                )
            )


            output[
                "vulnerabilities"
            ].append(
                cloned_vulnerability
            )


        if cloned_assets:
            current_first_asset = (
                cloned_assets[
                    0
                ][
                    "name"
                ]
            )

            current_last_asset = (
                cloned_assets[
                    -1
                ][
                    "name"
                ]
            )


            if (
                previous_last_asset
                is not None
                and current_first_asset
                in current_asset_names
            ):
                bridge = (
                    replace_strings(
                        copy.deepcopy(
                            relationship_template
                        ),
                        general_mapping,
                    )
                )


                bridge[
                    source_key
                ] = (
                    previous_last_asset
                )

                bridge[
                    target_key
                ] = (
                    current_first_asset
                )


                if "name" in bridge:
                    bridge[
                        "name"
                    ] = (
                        f"scale-bridge-"
                        f"{copy_number - 1}-"
                        f"{copy_number}"
                    )


                output[
                    "relationships"
                ].append(
                    bridge
                )


            previous_last_asset = (
                current_last_asset
            )


        generated_count += len(
            cloned_assets
        )


    return output


def main():
    parser = argparse.ArgumentParser()


    parser.add_argument(
        "--template",
        default=(
            "samples/ingestion/"
            "sample_environment.json"
        ),
    )

    parser.add_argument(
        "--assets",
        type=int,
        required=True,
    )

    parser.add_argument(
        "--output",
        required=True,
    )


    args = parser.parse_args()


    if args.assets < 1:
        raise SystemExit(
            "--assets must be positive."
        )


    template_path = Path(
        args.template
    )

    output_path = Path(
        args.output
    )


    template = json.loads(
        template_path.read_text(
            encoding="utf-8"
        )
    )


    environment = (
        build_scaled_environment(
            template,
            args.assets,
        )
    )


    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )


    output_path.write_text(
        json.dumps(
            environment,
            indent=2,
        ),

        encoding="utf-8",
    )


    print(
        (
            f"Generated "
            f"{len(environment['assets'])} "
            f"assets and "
            f"{len(environment['relationships'])} "
            f"relationships."
        )
    )

    print(
        f"Saved to {output_path}"
    )


if __name__ == "__main__":
    main()
