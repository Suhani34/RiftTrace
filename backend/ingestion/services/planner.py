from assets.models import (
    Asset,
    NetworkZone,
    Relationship,
)

from security.models import (
    Vulnerability,
)


ENTITY_NAMES = (
    "network_zones",
    "assets",
    "relationships",
    "vulnerabilities",
)


def _empty_summary():
    return {
        entity_name: {
            "create": 0,
            "update": 0,
            "unchanged": 0,
        }

        for entity_name
        in ENTITY_NAMES
    }


def _issue(
    issues,
    section,
    message,
):
    issues.append(
        {
            "section": section,
            "message": message,
        }
    )


def asset_ip_field_name():
    field_names = {
        field.name

        for field
        in Asset._meta.fields
    }


    if (
        "ip_address"
        in field_names
    ):
        return "ip_address"


    if "ip" in field_names:
        return "ip"


    return None


def _single_match(
    queryset,
    issues,
    section,
    description,
):
    count = queryset.count()


    if count > 1:
        _issue(
            issues,
            section,
            (
                f"Multiple existing "
                f"records match "
                f"{description}. "
                "Resolve the duplicates "
                "before importing."
            ),
        )

        return None


    if count == 1:
        return queryset.first()


    return None


def _duplicate_values(
    values,
):
    seen = set()

    duplicates = set()


    for value in values:
        key = value.casefold()


        if key in seen:
            duplicates.add(
                value
            )

        seen.add(
            key
        )


    return duplicates


def build_ingestion_plan(
    organization,
    bundle,
):
    summary = (
        _empty_summary()
    )

    issues = []


    zone_duplicates = (
        _duplicate_values(
            zone.name

            for zone
            in bundle.network_zones
        )
    )


    for name in sorted(
        zone_duplicates
    ):
        _issue(
            issues,
            "network_zones",
            (
                "Duplicate network zone "
                f"in import: {name}."
            ),
        )


    asset_duplicates = (
        _duplicate_values(
            asset.name

            for asset
            in bundle.assets
        )
    )


    for name in sorted(
        asset_duplicates
    ):
        _issue(
            issues,
            "assets",
            (
                "Duplicate asset name "
                f"in import: {name}."
            ),
        )


    relationship_keys = set()


    for relationship in (
        bundle.relationships
    ):
        key = (
            relationship
            .source_name
            .casefold(),

            relationship
            .target_name
            .casefold(),

            relationship
            .relationship_type,

            relationship
            .protocol
            .casefold(),

            relationship.port,
        )


        if key in relationship_keys:
            _issue(
                issues,
                "relationships",
                (
                    "Duplicate relationship "
                    "inside import: "
                    f"{relationship.source_name}"
                    " -> "
                    f"{relationship.target_name}"
                    "."
                ),
            )


        relationship_keys.add(
            key
        )


    vulnerability_keys = set()


    for vulnerability in (
        bundle.vulnerabilities
    ):
        identity = (
            vulnerability.reference_id

            or vulnerability.title
        )


        key = (
            vulnerability
            .asset_name
            .casefold(),

            identity.casefold(),
        )


        if key in vulnerability_keys:
            _issue(
                issues,
                "vulnerabilities",
                (
                    "Duplicate vulnerability "
                    "inside import: "
                    f"{identity} on "
                    f"{vulnerability.asset_name}."
                ),
            )


        vulnerability_keys.add(
            key
        )


    bundle_zone_names = {
        zone.name.casefold()

        for zone
        in bundle.network_zones
    }


    existing_zone_names = {
        name.casefold()

        for name
        in NetworkZone.objects.filter(
            organization=organization
        ).values_list(
            "name",
            flat=True,
        )
    }


    available_zone_names = (
        bundle_zone_names
        | existing_zone_names
    )


    bundle_asset_names = {
        asset.name.casefold()

        for asset
        in bundle.assets
    }


    existing_asset_names = {
        name.casefold()

        for name
        in Asset.objects.filter(
            organization=organization
        ).values_list(
            "name",
            flat=True,
        )
    }


    available_asset_names = (
        bundle_asset_names
        | existing_asset_names
    )


    for zone in (
        bundle.network_zones
    ):
        existing = _single_match(
            NetworkZone.objects.filter(
                organization=organization,

                name__iexact=(
                    zone.name
                ),
            ),

            issues,

            "network_zones",

            (
                "network zone "
                f"'{zone.name}'"
            ),
        )


        if existing is None:
            summary[
                "network_zones"
            ][
                "create"
            ] += 1

            continue


        if (
            existing.zone_type
            != zone.zone_type
        ):
            summary[
                "network_zones"
            ][
                "update"
            ] += 1

        else:
            summary[
                "network_zones"
            ][
                "unchanged"
            ] += 1


    ip_field = (
        asset_ip_field_name()
    )


    for asset in bundle.assets:
        if (
            asset.network_zone_name
            and (
                asset
                .network_zone_name
                .casefold()
                not in
                available_zone_names
            )
        ):
            _issue(
                issues,
                "assets",
                (
                    f"Asset '{asset.name}' "
                    "references unknown "
                    "network zone "
                    f"'{asset.network_zone_name}'."
                ),
            )


        existing = _single_match(
            Asset.objects.filter(
                organization=organization,

                name__iexact=(
                    asset.name
                ),
            ),

            issues,

            "assets",

            (
                f"asset '{asset.name}'"
            ),
        )


        if existing is None:
            summary[
                "assets"
            ][
                "create"
            ] += 1

            continue


        existing_zone_name = (
            existing.network_zone.name

            if existing.network_zone

            else None
        )


        desired_state = {
            "asset_type":
                asset.asset_type,

            "criticality":
                asset.criticality,

            "environment":
                asset.environment,

            "hostname":
                asset.hostname,

            "is_internet_exposed":
                asset
                .is_internet_exposed,

            "network_zone":
                asset
                .network_zone_name,
        }


        current_state = {
            "asset_type":
                existing.asset_type,

            "criticality":
                existing.criticality,

            "environment":
                existing.environment,

            "hostname":
                existing.hostname,

            "is_internet_exposed":
                existing
                .is_internet_exposed,

            "network_zone":
                existing_zone_name,
        }


        if ip_field:
            desired_state[
                ip_field
            ] = asset.ip_address

            current_state[
                ip_field
            ] = getattr(
                existing,
                ip_field,
            )


        if (
            current_state
            == desired_state
        ):
            summary[
                "assets"
            ][
                "unchanged"
            ] += 1

        else:
            summary[
                "assets"
            ][
                "update"
            ] += 1


    for relationship in (
        bundle.relationships
    ):
        if (
            relationship
            .source_name
            .casefold()
            not in available_asset_names
        ):
            _issue(
                issues,
                "relationships",
                (
                    "Unknown relationship "
                    "source asset: "
                    f"{relationship.source_name}."
                ),
            )


        if (
            relationship
            .target_name
            .casefold()
            not in available_asset_names
        ):
            _issue(
                issues,
                "relationships",
                (
                    "Unknown relationship "
                    "target asset: "
                    f"{relationship.target_name}."
                ),
            )


        source = (
            Asset.objects.filter(
                organization=organization,

                name__iexact=(
                    relationship
                    .source_name
                ),
            )
            .order_by("id")
            .first()
        )


        target = (
            Asset.objects.filter(
                organization=organization,

                name__iexact=(
                    relationship
                    .target_name
                ),
            )
            .order_by("id")
            .first()
        )


        if (
            source is None
            or target is None
        ):
            if (
                relationship
                .source_name
                .casefold()
                in bundle_asset_names

                or

                relationship
                .target_name
                .casefold()
                in bundle_asset_names
            ):
                summary[
                    "relationships"
                ][
                    "create"
                ] += 1

            continue


        queryset = (
            Relationship.objects.filter(
                source=source,

                target=target,

                relationship_type=(
                    relationship
                    .relationship_type
                ),

                protocol=(
                    relationship.protocol
                ),

                port=(
                    relationship.port
                ),
            )
        )


        existing = _single_match(
            queryset,

            issues,

            "relationships",

            (
                "relationship "
                f"{relationship.source_name}"
                " -> "
                f"{relationship.target_name}"
            ),
        )


        if existing is None:
            summary[
                "relationships"
            ][
                "create"
            ] += 1

            continue


        if (
            existing
            .requires_authentication
            == relationship
            .requires_authentication

            and

            existing
            .required_source_privilege
            == relationship
            .required_source_privilege
        ):
            summary[
                "relationships"
            ][
                "unchanged"
            ] += 1

        else:
            summary[
                "relationships"
            ][
                "update"
            ] += 1


    for vulnerability in (
        bundle.vulnerabilities
    ):
        if (
            vulnerability
            .asset_name
            .casefold()
            not in available_asset_names
        ):
            _issue(
                issues,
                "vulnerabilities",
                (
                    "Unknown vulnerability "
                    "asset: "
                    f"{vulnerability.asset_name}."
                ),
            )


        asset = (
            Asset.objects.filter(
                organization=organization,

                name__iexact=(
                    vulnerability
                    .asset_name
                ),
            )
            .order_by("id")
            .first()
        )


        if asset is None:
            if (
                vulnerability
                .asset_name
                .casefold()
                in bundle_asset_names
            ):
                summary[
                    "vulnerabilities"
                ][
                    "create"
                ] += 1

            continue


        if vulnerability.reference_id:
            queryset = (
                Vulnerability.objects.filter(
                    asset=asset,

                    reference_id__iexact=(
                        vulnerability
                        .reference_id
                    ),
                )
            )

        else:
            queryset = (
                Vulnerability.objects.filter(
                    asset=asset,

                    title__iexact=(
                        vulnerability.title
                    ),
                )
            )


        existing = _single_match(
            queryset,

            issues,

            "vulnerabilities",

            (
                "vulnerability "
                f"'{vulnerability.reference_id or vulnerability.title}' "
                f"on '{vulnerability.asset_name}'"
            ),
        )


        if existing is None:
            summary[
                "vulnerabilities"
            ][
                "create"
            ] += 1

            continue


        desired_state = {
            "title":
                vulnerability.title,

            "reference_id":
                vulnerability
                .reference_id,

            "cvss_score":
                vulnerability
                .cvss_score,

            "attack_vector":
                vulnerability
                .attack_vector,

            "privileges_required":
                vulnerability
                .privileges_required,

            "grants_privilege":
                vulnerability
                .grants_privilege,

            "bypasses_authentication":
                vulnerability
                .bypasses_authentication,

            "bypasses_mfa":
                vulnerability
                .bypasses_mfa,

            "is_exploitable":
                vulnerability
                .is_exploitable,

            "description":
                vulnerability
                .description,
        }


        current_state = {
            key:
                getattr(
                    existing,
                    key,
                )

            for key
            in desired_state
        }


        if (
            current_state
            == desired_state
        ):
            summary[
                "vulnerabilities"
            ][
                "unchanged"
            ] += 1

        else:
            summary[
                "vulnerabilities"
            ][
                "update"
            ] += 1


    normalized_counts = {
        "network_zones":
            len(
                bundle.network_zones
            ),

        "assets":
            len(
                bundle.assets
            ),

        "relationships":
            len(
                bundle.relationships
            ),

        "vulnerabilities":
            len(
                bundle.vulnerabilities
            ),
    }


    return {
        "valid":
            len(
                issues
            )
            == 0,

        "normalized_counts":
            normalized_counts,

        "summary":
            summary,

        "issues":
            issues,

        "source_files":
            list(
                bundle.source_files
            ),
    }
