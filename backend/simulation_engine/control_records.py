from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class SecurityControlRecord:
    id: int

    name: str

    control_type: str

    target_relationship_id: (
        int | None
    )

    target_vulnerability_id: (
        int | None
    )
