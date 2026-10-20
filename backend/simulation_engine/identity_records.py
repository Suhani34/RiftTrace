from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class IdentityRecord:
    id: int

    name: str

    identity_type: str

    privilege_level: str

    enabled: bool


@dataclass(
    frozen=True,
    slots=True,
)
class CredentialExposureRecord:
    id: int

    name: str

    identity_id: int

    stored_on_asset_id: int

    credential_type: str

    discoverable_on_compromise: bool

    satisfies_mfa: bool

    active: bool


@dataclass(
    frozen=True,
    slots=True,
)
class IdentityAccessRecord:
    id: int

    identity_id: int

    asset_id: int

    access_type: str

    granted_privilege: str

    requires_mfa: bool

    enabled: bool


@dataclass(
    frozen=True,
    slots=True,
)
class IdentityLinkRecord:
    id: int

    source_identity_id: int

    target_identity_id: int

    link_type: str

    requires_mfa: bool

    enabled: bool


@dataclass(
    frozen=True,
    slots=True,
)
class AcquiredIdentity:
    identity_id: int

    mfa_satisfied: bool


@dataclass(
    frozen=True,
    slots=True,
)
class IdentityPropagationStep:
    step_type: str

    source_kind: str

    source_id: int

    target_kind: str

    target_id: int

    reference_id: int

    detail: str


@dataclass(
    frozen=True,
    slots=True,
)
class BlockedIdentityStep:
    step_type: str

    source_kind: str

    source_id: int

    target_kind: str

    target_id: int

    reference_id: int

    reason: str


@dataclass(
    frozen=True,
    slots=True,
)
class IdentityPropagationResult:
    compromised_assets: tuple[
        tuple[int, str],
        ...,
    ]

    acquired_identities: tuple[
        AcquiredIdentity,
        ...,
    ]

    steps: tuple[
        IdentityPropagationStep,
        ...,
    ]

    blocked_steps: tuple[
        BlockedIdentityStep,
        ...,
    ]
