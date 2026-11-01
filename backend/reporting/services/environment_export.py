import hashlib
import json

from django.utils import timezone

from assets.models import (
    Asset,
    NetworkZone,
    Relationship,
)

from security.models import (
    Vulnerability,
)

from reporting.constants import (
    ENVIRONMENT_SCHEMA,
    SCHEMA_VERSION,
)


def _canonical_json(
    value,
):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(
            ",",
            ":",
        ),
        default=str,
    )


def _payload_sha256(
    value,
):
    encoded = (
        _canonical_json(
            value
        )
        .encode(
            "utf-8"
        )
    )


    return (
        hashlib.sha256(
            encoded
        )
        .hexdigest()
    )


def build_ingestion_environment(
    organization,
):
    zones = (
        NetworkZone.objects
        .filter(
            organization=organization
        )
        .order_by(
            "id"
        )
    )


    assets = (
        Asset.objects
        .filter(
            organization=organization
        )
        .select_related(
            "network_zone"
        )
        .order_by(
            "id"
        )
    )


    relationships = (
        Relationship.objects
        .filter(
            source__organization=(
                organization
            )
        )
        .select_related(
            "source",
            "target",
        )
        .order_by(
            "id"
        )
    )


    vulnerabilities = (
        Vulnerability.objects
        .filter(
            asset__organization=(
                organization
            )
        )
        .select_related(
            "asset"
        )
        .order_by(
            "id"
        )
    )


    return {
        "network_zones": [
            {
                "name":
                    zone.name,

                "zone_type":
                    zone.zone_type,

                "description":
                    zone.description,
            }

            for zone
            in zones
        ],

        "assets": [
            {
                "name":
                    asset.name,

                "asset_type":
                    asset.asset_type,

                "criticality":
                    asset.criticality,

                "environment":
                    asset.environment,

                "network_zone":
                    (
                        asset
                        .network_zone
                        .name

                        if asset.network_zone
                        else None
                    ),

                "hostname":
                    asset.hostname,

                "ip_address":
                    asset.ip_address,

                "description":
                    asset.description,

                "is_internet_exposed":
                    asset.is_internet_exposed,
            }

            for asset
            in assets
        ],

        "relationships": [
            {
                "source":
                    relationship
                    .source
                    .name,

                "target":
                    relationship
                    .target
                    .name,

                "relationship_type":
                    relationship
                    .relationship_type,

                "protocol":
                    relationship.protocol,

                "port":
                    relationship.port,

                "requires_authentication":
                    relationship
                    .requires_authentication,

                "required_source_privilege":
                    relationship
                    .required_source_privilege,

                "description":
                    relationship.description,
            }

            for relationship
            in relationships
        ],

        "vulnerabilities": [
            {
                "asset":
                    vulnerability
                    .asset
                    .name,

                "title":
                    vulnerability.title,

                "reference_id":
                    vulnerability
                    .reference_id,

                "cvss_score":
                    (
                        float(
                            vulnerability
                            .cvss_score
                        )

                        if (
                            vulnerability
                            .cvss_score
                            is not None
                        )
                        else None
                    ),

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
                    vulnerability.description,
            }

            for vulnerability
            in vulnerabilities
        ],
    }


def build_portable_environment(
    organization,
):
    data = (
        build_ingestion_environment(
            organization
        )
    )


    return {
        "schema":
            ENVIRONMENT_SCHEMA,

        "schema_version":
            SCHEMA_VERSION,

        "generated_at":
            timezone.now()
            .isoformat(),

        "organization": {
            "id":
                organization.id,

            "name":
                organization.name,

            "description":
                organization.description,
        },

        "payload_sha256":
            _payload_sha256(
                data
            ),

        "data":
            data,
    }
