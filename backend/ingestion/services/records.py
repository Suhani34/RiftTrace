from dataclasses import (
    dataclass,
)

from decimal import Decimal


@dataclass(
    frozen=True,
    slots=True,
)
class NetworkZoneInput:
    name: str

    zone_type: str


@dataclass(
    frozen=True,
    slots=True,
)
class AssetInput:
    name: str

    asset_type: str

    criticality: str

    environment: str

    network_zone_name: (
        str | None
    )

    hostname: str

    ip_address: str

    is_internet_exposed: bool


@dataclass(
    frozen=True,
    slots=True,
)
class RelationshipInput:
    source_name: str

    target_name: str

    relationship_type: str

    protocol: str

    port: int | None

    requires_authentication: bool

    required_source_privilege: str


@dataclass(
    frozen=True,
    slots=True,
)
class VulnerabilityInput:
    asset_name: str

    reference_id: str

    title: str

    cvss_score: (
        Decimal | None
    )

    attack_vector: str

    privileges_required: str

    grants_privilege: str

    bypasses_authentication: bool

    bypasses_mfa: bool

    is_exploitable: bool

    description: str


@dataclass(
    frozen=True,
    slots=True,
)
class IngestionBundle:
    network_zones: tuple[
        NetworkZoneInput,
        ...,
    ]

    assets: tuple[
        AssetInput,
        ...,
    ]

    relationships: tuple[
        RelationshipInput,
        ...,
    ]

    vulnerabilities: tuple[
        VulnerabilityInput,
        ...,
    ]

    source_files: tuple[
        str,
        ...,
    ]
