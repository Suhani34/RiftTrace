from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class BusinessProcessRecord:
    id: int

    name: str

    criticality: str

    impact_description: str


@dataclass(
    frozen=True,
    slots=True,
)
class BusinessDependencyRecord:
    id: int

    business_process_id: int

    asset_id: int

    dependency_level: str
