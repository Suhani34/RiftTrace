from .identity_records import (
    AcquiredIdentity,
    BlockedIdentityStep,
    CredentialExposureRecord,
    IdentityAccessRecord,
    IdentityLinkRecord,
    IdentityPropagationResult,
    IdentityPropagationStep,
    IdentityRecord,
)


def _privilege_rank(
    privilege,
):
    return {
        "LOW": 1,
        "HIGH": 2,
    }.get(
        privilege,
        0,
    )


def _should_upgrade_privilege(
    current,
    candidate,
):
    return (
        _privilege_rank(
            candidate
        )
        >
        _privilege_rank(
            current
        )
    )


def analyze_identity_propagation(
    *,
    compromised_assets,
    identities,
    credentials,
    accesses,
    links,
):
    """
    Expand a set of already-compromised assets
    through modeled credential and identity paths.

    compromised_assets:
        dict[int, str]

        Example:
        {
            1: "LOW",
            4: "HIGH",
        }
    """

    compromised = dict(
        compromised_assets
    )


    identities_by_id = {
        identity.id: identity

        for identity
        in identities
    }


    acquired = {}


    steps = []

    blocked_steps = []


    step_keys = set()

    blocked_keys = set()


    changed = True


    while changed:
        changed = False


        # -------------------------------------------------
        # 1. Discover credentials on compromised assets
        # -------------------------------------------------

        for credential in credentials:
            if not credential.active:
                continue


            if not (
                credential
                .discoverable_on_compromise
            ):
                continue


            if (
                credential
                .stored_on_asset_id
                not in compromised
            ):
                continue


            identity = identities_by_id.get(
                credential.identity_id
            )


            if (
                identity is None
                or not identity.enabled
            ):
                continue


            previous_mfa = acquired.get(
                identity.id
            )


            candidate_mfa = (
                credential.satisfies_mfa
            )


            should_record = False


            if previous_mfa is None:
                acquired[
                    identity.id
                ] = candidate_mfa

                changed = True

                should_record = True


            elif (
                candidate_mfa
                and not previous_mfa
            ):
                acquired[
                    identity.id
                ] = True

                changed = True

                should_record = True


            if should_record:
                key = (
                    "CREDENTIAL_DISCOVERY",
                    credential.id,
                    identity.id,
                )


                if key not in step_keys:
                    step_keys.add(
                        key
                    )


                    steps.append(
                        IdentityPropagationStep(
                            step_type=(
                                "CREDENTIAL_DISCOVERY"
                            ),

                            source_kind=(
                                "ASSET"
                            ),

                            source_id=(
                                credential
                                .stored_on_asset_id
                            ),

                            target_kind=(
                                "IDENTITY"
                            ),

                            target_id=(
                                identity.id
                            ),

                            reference_id=(
                                credential.id
                            ),

                            detail=(
                                "Credential exposure "
                                "made the identity "
                                "available."
                            ),
                        )
                    )


        # -------------------------------------------------
        # 2. Traverse identity-to-identity links
        # -------------------------------------------------

        for link in links:
            if not link.enabled:
                continue


            if (
                link.source_identity_id
                not in acquired
            ):
                continue


            source_mfa = acquired[
                link.source_identity_id
            ]


            target_identity = (
                identities_by_id.get(
                    link.target_identity_id
                )
            )


            if (
                target_identity is None
                or not target_identity.enabled
            ):
                continue


            if (
                link.requires_mfa
                and not source_mfa
            ):
                key = (
                    "IDENTITY_LINK",
                    link.id,
                    "MFA_REQUIRED",
                )


                if key not in blocked_keys:
                    blocked_keys.add(
                        key
                    )


                    blocked_steps.append(
                        BlockedIdentityStep(
                            step_type=(
                                "IDENTITY_LINK"
                            ),

                            source_kind=(
                                "IDENTITY"
                            ),

                            source_id=(
                                link
                                .source_identity_id
                            ),

                            target_kind=(
                                "IDENTITY"
                            ),

                            target_id=(
                                link
                                .target_identity_id
                            ),

                            reference_id=(
                                link.id
                            ),

                            reason=(
                                "MFA_REQUIRED"
                            ),
                        )
                    )


                continue


            target_previous_mfa = (
                acquired.get(
                    link.target_identity_id
                )
            )


            target_candidate_mfa = (
                source_mfa
            )


            should_record = False


            if target_previous_mfa is None:
                acquired[
                    link.target_identity_id
                ] = target_candidate_mfa

                changed = True

                should_record = True


            elif (
                target_candidate_mfa
                and not target_previous_mfa
            ):
                acquired[
                    link.target_identity_id
                ] = True

                changed = True

                should_record = True


            if should_record:
                key = (
                    "IDENTITY_LINK",
                    link.id,
                    link.target_identity_id,
                )


                if key not in step_keys:
                    step_keys.add(
                        key
                    )


                    steps.append(
                        IdentityPropagationStep(
                            step_type=(
                                "IDENTITY_LINK"
                            ),

                            source_kind=(
                                "IDENTITY"
                            ),

                            source_id=(
                                link
                                .source_identity_id
                            ),

                            target_kind=(
                                "IDENTITY"
                            ),

                            target_id=(
                                link
                                .target_identity_id
                            ),

                            reference_id=(
                                link.id
                            ),

                            detail=(
                                link.link_type
                            ),
                        )
                    )


        # -------------------------------------------------
        # 3. Use identities to reach assets
        # -------------------------------------------------

        for access in accesses:
            if not access.enabled:
                continue


            if (
                access.identity_id
                not in acquired
            ):
                continue


            identity = identities_by_id.get(
                access.identity_id
            )


            if (
                identity is None
                or not identity.enabled
            ):
                continue


            identity_mfa = acquired[
                access.identity_id
            ]


            if (
                access.requires_mfa
                and not identity_mfa
            ):
                key = (
                    "IDENTITY_ACCESS",
                    access.id,
                    "MFA_REQUIRED",
                )


                if key not in blocked_keys:
                    blocked_keys.add(
                        key
                    )


                    blocked_steps.append(
                        BlockedIdentityStep(
                            step_type=(
                                "IDENTITY_ACCESS"
                            ),

                            source_kind=(
                                "IDENTITY"
                            ),

                            source_id=(
                                access.identity_id
                            ),

                            target_kind=(
                                "ASSET"
                            ),

                            target_id=(
                                access.asset_id
                            ),

                            reference_id=(
                                access.id
                            ),

                            reason=(
                                "MFA_REQUIRED"
                            ),
                        )
                    )


                continue


            existing_privilege = (
                compromised.get(
                    access.asset_id
                )
            )


            should_record = False


            if existing_privilege is None:
                compromised[
                    access.asset_id
                ] = (
                    access
                    .granted_privilege
                )

                changed = True

                should_record = True


            elif _should_upgrade_privilege(
                existing_privilege,

                access.granted_privilege,
            ):
                compromised[
                    access.asset_id
                ] = (
                    access
                    .granted_privilege
                )

                changed = True

                should_record = True


            if should_record:
                key = (
                    "IDENTITY_ACCESS",
                    access.id,
                    access.asset_id,
                    compromised[
                        access.asset_id
                    ],
                )


                if key not in step_keys:
                    step_keys.add(
                        key
                    )


                    steps.append(
                        IdentityPropagationStep(
                            step_type=(
                                "IDENTITY_ACCESS"
                            ),

                            source_kind=(
                                "IDENTITY"
                            ),

                            source_id=(
                                access.identity_id
                            ),

                            target_kind=(
                                "ASSET"
                            ),

                            target_id=(
                                access.asset_id
                            ),

                            reference_id=(
                                access.id
                            ),

                            detail=(
                                access.access_type
                            ),
                        )
                    )


    return IdentityPropagationResult(
        compromised_assets=tuple(
            sorted(
                compromised.items()
            )
        ),

        acquired_identities=tuple(
            AcquiredIdentity(
                identity_id=identity_id,

                mfa_satisfied=(
                    mfa_satisfied
                ),
            )

            for (
                identity_id,
                mfa_satisfied,
            )
            in sorted(
                acquired.items()
            )
        ),

        steps=tuple(
            steps
        ),

        blocked_steps=tuple(
            blocked_steps
        ),
    )
