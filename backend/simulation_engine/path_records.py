from dataclasses import dataclass


@dataclass(
    frozen=True
)
class AttackTransition:
    relationship_id: int

    source_asset_id: int
    source_asset_name: str
    source_privilege: str

    target_asset_id: int
    target_asset_name: str
    target_privilege: str

    mechanism: str

    vulnerability_id: int | None = None
    vulnerability_title: str | None = None


@dataclass(
    frozen=True
)
class PathTargetMetadata:
    asset_id: int
    asset_name: str
    criticality: str

    business_processes: tuple[
        str,
        ...,
    ] = ()

    critical_business_processes: tuple[
        str,
        ...,
    ] = ()
