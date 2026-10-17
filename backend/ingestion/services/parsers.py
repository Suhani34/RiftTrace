import csv
import io
import json

from decimal import (
    Decimal,
    InvalidOperation,
)

from assets.models import (
    Asset,
    NetworkZone,
    Relationship,
)

from security.models import (
    Vulnerability,
)

from .records import (
    AssetInput,
    IngestionBundle,
    NetworkZoneInput,
    RelationshipInput,
    VulnerabilityInput,
)


class IngestionParseError(
    ValueError
):
    pass


def _text(
    value,
) -> str:
    if value is None:
        return ""

    return str(value).strip()


def _required_text(
    value,
    field_name,
    section,
    row_number,
) -> str:
    result = _text(
        value
    )


    if not result:
        raise IngestionParseError(
            (
                f"{section} row "
                f"{row_number}: "
                f"{field_name} is required."
            )
        )


    return result


def _choice(
    model,
    field_name,
    value,
    section,
    row_number,
) -> str:
    raw_value = _required_text(
        value,
        field_name,
        section,
        row_number,
    )


    field = model._meta.get_field(
        field_name
    )


    for (
        stored_value,
        label,
    ) in field.flatchoices:
        if (
            str(
                stored_value
            ).casefold()
            == raw_value.casefold()
        ):
            return str(
                stored_value
            )


        if (
            str(
                label
            ).casefold()
            == raw_value.casefold()
        ):
            return str(
                stored_value
            )


    allowed = ", ".join(
        str(
            stored_value
        )

        for (
            stored_value,
            _,
        )
        in field.flatchoices
    )


    raise IngestionParseError(
        (
            f"{section} row "
            f"{row_number}: "
            f"invalid {field_name} "
            f"'{raw_value}'. "
            f"Allowed values: "
            f"{allowed}."
        )
    )


def _boolean(
    value,
    default=False,
) -> bool:
    if value is None:
        return default


    if isinstance(
        value,
        bool,
    ):
        return value


    text = _text(
        value
    ).casefold()


    if not text:
        return default


    if text in {
        "true",
        "1",
        "yes",
        "y",
    }:
        return True


    if text in {
        "false",
        "0",
        "no",
        "n",
    }:
        return False


    raise IngestionParseError(
        (
            "Boolean values must be "
            "true/false, yes/no or 1/0."
        )
    )


def _optional_integer(
    value,
) -> int | None:
    text = _text(
        value
    )


    if not text:
        return None


    try:
        return int(
            text
        )

    except ValueError as exc:
        raise IngestionParseError(
            f"Invalid integer: {text}."
        ) from exc


def _optional_decimal(
    value,
) -> Decimal | None:
    text = _text(
        value
    )


    if not text:
        return None


    try:
        return Decimal(
            text
        )

    except InvalidOperation as exc:
        raise IngestionParseError(
            (
                f"Invalid decimal value: "
                f"{text}."
            )
        ) from exc


def _parse_zone(
    raw,
    row_number,
):
    return NetworkZoneInput(
        name=_required_text(
            raw.get("name"),
            "name",
            "network_zones",
            row_number,
        ),

        zone_type=_choice(
            NetworkZone,
            "zone_type",
            raw.get("zone_type"),
            "network_zones",
            row_number,
        ),
    )


def _parse_asset(
    raw,
    row_number,
):
    ip_address = (
        raw.get(
            "ip_address"
        )

        if (
            "ip_address"
            in raw
        )

        else raw.get(
            "ip"
        )
    )


    return AssetInput(
        name=_required_text(
            raw.get("name"),
            "name",
            "assets",
            row_number,
        ),

        asset_type=_choice(
            Asset,
            "asset_type",
            raw.get("asset_type"),
            "assets",
            row_number,
        ),

        criticality=_choice(
            Asset,
            "criticality",
            raw.get("criticality"),
            "assets",
            row_number,
        ),

        environment=_choice(
            Asset,
            "environment",
            raw.get("environment"),
            "assets",
            row_number,
        ),

        network_zone_name=(
            _text(
                raw.get(
                    "network_zone"
                )
            )
            or None
        ),

        hostname=_text(
            raw.get(
                "hostname"
            )
        ),

        ip_address=_text(
            ip_address
        ),

        is_internet_exposed=_boolean(
            raw.get(
                "is_internet_exposed"
            ),

            default=False,
        ),
    )


def _parse_relationship(
    raw,
    row_number,
):
    port = _optional_integer(
        raw.get(
            "port"
        )
    )


    if (
        port is not None
        and (
            port < 1
            or port > 65535
        )
    ):
        raise IngestionParseError(
            (
                "relationships row "
                f"{row_number}: "
                "port must be between "
                "1 and 65535."
            )
        )


    required_privilege = (
        raw.get(
            "required_source_privilege"
        )

        or "LOW"
    )


    return RelationshipInput(
        source_name=_required_text(
            raw.get("source"),
            "source",
            "relationships",
            row_number,
        ),

        target_name=_required_text(
            raw.get("target"),
            "target",
            "relationships",
            row_number,
        ),

        relationship_type=_choice(
            Relationship,
            "relationship_type",
            raw.get(
                "relationship_type"
            ),
            "relationships",
            row_number,
        ),

        protocol=_text(
            raw.get(
                "protocol"
            )
        ),

        port=port,

        requires_authentication=(
            _boolean(
                raw.get(
                    "requires_authentication"
                ),

                default=False,
            )
        ),

        required_source_privilege=(
            _choice(
                Relationship,
                "required_source_privilege",
                required_privilege,
                "relationships",
                row_number,
            )
        ),
    )


def _parse_vulnerability(
    raw,
    row_number,
):
    return VulnerabilityInput(
        asset_name=_required_text(
            raw.get("asset"),
            "asset",
            "vulnerabilities",
            row_number,
        ),

        reference_id=_text(
            raw.get(
                "reference_id"
            )
        ),

        title=_required_text(
            raw.get("title"),
            "title",
            "vulnerabilities",
            row_number,
        ),

        cvss_score=(
            _optional_decimal(
                raw.get(
                    "cvss_score"
                )
            )
        ),

        attack_vector=_choice(
            Vulnerability,
            "attack_vector",
            raw.get(
                "attack_vector"
            ),
            "vulnerabilities",
            row_number,
        ),

        privileges_required=_choice(
            Vulnerability,
            "privileges_required",
            raw.get(
                "privileges_required"
            ),
            "vulnerabilities",
            row_number,
        ),

        grants_privilege=_choice(
            Vulnerability,
            "grants_privilege",
            raw.get(
                "grants_privilege"
            ),
            "vulnerabilities",
            row_number,
        ),

        bypasses_authentication=(
            _boolean(
                raw.get(
                    "bypasses_authentication"
                ),

                default=False,
            )
        ),

        bypasses_mfa=(
            _boolean(
                raw.get(
                    "bypasses_mfa"
                ),

                default=False,
            )
        ),

        is_exploitable=(
            _boolean(
                raw.get(
                    "is_exploitable"
                ),

                default=True,
            )
        ),

        description=_text(
            raw.get(
                "description"
            )
        ),
    )


def _decode_uploaded_file(
    uploaded_file,
) -> str:
    try:
        return (
            uploaded_file
            .read()
            .decode(
                "utf-8-sig"
            )
        )

    except UnicodeDecodeError as exc:
        raise IngestionParseError(
            (
                "Uploaded files must use "
                "UTF-8 encoding."
            )
        ) from exc


def _csv_rows(
    uploaded_file,
):
    content = (
        _decode_uploaded_file(
            uploaded_file
        )
    )


    reader = csv.DictReader(
        io.StringIO(
            content
        )
    )


    if reader.fieldnames is None:
        raise IngestionParseError(
            (
                f"{uploaded_file.name} "
                "has no CSV header."
            )
        )


    return list(
        reader
    )


def parse_json_bundle(
    uploaded_file,
) -> IngestionBundle:
    content = (
        _decode_uploaded_file(
            uploaded_file
        )
    )


    try:
        raw_bundle = json.loads(
            content
        )

    except json.JSONDecodeError as exc:
        raise IngestionParseError(
            (
                "The uploaded JSON file "
                "is not valid JSON."
            )
        ) from exc


    if not isinstance(
        raw_bundle,
        dict,
    ):
        raise IngestionParseError(
            (
                "The top-level JSON "
                "value must be an object."
            )
        )


    def section(
        name,
    ):
        value = raw_bundle.get(
            name,
            [],
        )


        if not isinstance(
            value,
            list,
        ):
            raise IngestionParseError(
                (
                    f"'{name}' must "
                    "be a JSON array."
                )
            )


        return value


    raw_zones = section(
        "network_zones"
    )

    raw_assets = section(
        "assets"
    )

    raw_relationships = section(
        "relationships"
    )

    raw_vulnerabilities = section(
        "vulnerabilities"
    )


    if not any(
        (
            raw_zones,
            raw_assets,
            raw_relationships,
            raw_vulnerabilities,
        )
    ):
        raise IngestionParseError(
            (
                "The JSON bundle contains "
                "no importable records."
            )
        )


    return IngestionBundle(
        network_zones=tuple(
            _parse_zone(
                row,
                index,
            )

            for index, row
            in enumerate(
                raw_zones,
                start=1,
            )
        ),

        assets=tuple(
            _parse_asset(
                row,
                index,
            )

            for index, row
            in enumerate(
                raw_assets,
                start=1,
            )
        ),

        relationships=tuple(
            _parse_relationship(
                row,
                index,
            )

            for index, row
            in enumerate(
                raw_relationships,
                start=1,
            )
        ),

        vulnerabilities=tuple(
            _parse_vulnerability(
                row,
                index,
            )

            for index, row
            in enumerate(
                raw_vulnerabilities,
                start=1,
            )
        ),

        source_files=(
            uploaded_file.name,
        ),
    )


def parse_csv_bundle(
    *,
    network_zones_file=None,
    assets_file=None,
    relationships_file=None,
    vulnerabilities_file=None,
) -> IngestionBundle:
    source_files = []


    raw_zones = []

    raw_assets = []

    raw_relationships = []

    raw_vulnerabilities = []


    if network_zones_file:
        source_files.append(
            network_zones_file.name
        )

        raw_zones = _csv_rows(
            network_zones_file
        )


    if assets_file:
        source_files.append(
            assets_file.name
        )

        raw_assets = _csv_rows(
            assets_file
        )


    if relationships_file:
        source_files.append(
            relationships_file.name
        )

        raw_relationships = (
            _csv_rows(
                relationships_file
            )
        )


    if vulnerabilities_file:
        source_files.append(
            vulnerabilities_file.name
        )

        raw_vulnerabilities = (
            _csv_rows(
                vulnerabilities_file
            )
        )


    if not source_files:
        raise IngestionParseError(
            (
                "At least one CSV file "
                "must be uploaded."
            )
        )


    return IngestionBundle(
        network_zones=tuple(
            _parse_zone(
                row,
                index,
            )

            for index, row
            in enumerate(
                raw_zones,
                start=2,
            )
        ),

        assets=tuple(
            _parse_asset(
                row,
                index,
            )

            for index, row
            in enumerate(
                raw_assets,
                start=2,
            )
        ),

        relationships=tuple(
            _parse_relationship(
                row,
                index,
            )

            for index, row
            in enumerate(
                raw_relationships,
                start=2,
            )
        ),

        vulnerabilities=tuple(
            _parse_vulnerability(
                row,
                index,
            )

            for index, row
            in enumerate(
                raw_vulnerabilities,
                start=2,
            )
        ),

        source_files=tuple(
            source_files
        ),
    )

def parse_ingestion_upload(
    validated_data,
):
    source_format = (
        validated_data[
            "source_format"
        ]
    )


    if source_format == "JSON":
        return parse_json_bundle(
            validated_data[
                "bundle_file"
            ]
        )


    return parse_csv_bundle(
        network_zones_file=(
            validated_data.get(
                "network_zones_file"
            )
        ),

        assets_file=(
            validated_data.get(
                "assets_file"
            )
        ),

        relationships_file=(
            validated_data.get(
                "relationships_file"
            )
        ),

        vulnerabilities_file=(
            validated_data.get(
                "vulnerabilities_file"
            )
        ),
    )
