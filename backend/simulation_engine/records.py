from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class AssetRecord:
    id: int
    name: str

    asset_type: str
    criticality: str
    environment: str

    network_zone_id: int | None

    is_internet_exposed: bool


@dataclass(
    frozen=True,
    slots=True,
)
class RelationshipRecord:
    id: int

    source_id: int
    target_id: int

    relationship_type: str

    protocol: str
    port: int | None

    requires_authentication: bool
    required_source_privilege: str

@dataclass(
    frozen=True,
    slots=True,
)
class VulnerabilityRecord:
    id: int

    asset_id: int

    title: str
    reference_id: str

    attack_vector: str

    privileges_required: str

    grants_privilege: str

    bypasses_authentication: bool

    is_exploitable: bool
