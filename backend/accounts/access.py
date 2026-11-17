from rest_framework.exceptions import (
    PermissionDenied,
)

from organizations.models import (
    Organization,
)

from .models import (
    OrganizationMembership,
)


ROLE_LEVEL = {
    OrganizationMembership
    .Role
    .VIEWER: 1,

    OrganizationMembership
    .Role
    .ANALYST: 2,

    OrganizationMembership
    .Role
    .ADMIN: 3,
}


def organizations_for_user(
    user,
):
    if not user.is_authenticated:
        return Organization.objects.none()


    if user.is_superuser:
        return Organization.objects.all()


    return (
        Organization.objects
        .filter(
            memberships__user=user
        )
        .distinct()
    )


def get_membership(
    user,
    organization,
):
    if user.is_superuser:
        return None


    try:
        return (
            OrganizationMembership
            .objects
            .get(
                user=user,
                organization=(
                    organization
                ),
            )
        )

    except (
        OrganizationMembership
        .DoesNotExist
    ) as exc:
        raise PermissionDenied(
            (
                "You do not have "
                "access to this "
                "organization."
            )
        ) from exc


def ensure_organization_access(
    user,
    organization,
):
    if user.is_superuser:
        return


    get_membership(
        user,
        organization,
    )


def ensure_organization_role(
    user,
    organization,
    minimum_role,
):
    if user.is_superuser:
        return


    membership = get_membership(
        user,
        organization,
    )


    user_level = (
        ROLE_LEVEL[
            membership.role
        ]
    )


    required_level = (
        ROLE_LEVEL[
            minimum_role
        ]
    )


    if user_level < required_level:
        raise PermissionDenied(
            (
                "Your organization "
                "role does not allow "
                "this action."
            )
        )
