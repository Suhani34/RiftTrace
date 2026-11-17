from django.contrib.auth import (
    get_user_model,
)

from rest_framework.test import (
    APITestCase,
)


class AuthenticatedAPITestCase(
    APITestCase
):
    """
    Base class for RiftTrace's existing API
    regression tests.

    These tests existed before authentication
    was introduced and are intended to test
    API functionality rather than permissions.

    A superuser is therefore authenticated
    automatically before every test.

    Phase 1 security tests must NOT inherit
    from this class.
    """

    def _pre_setup(self):
        super()._pre_setup()


        User = get_user_model()


        self.authenticated_test_user = (
            User.objects.create_superuser(
                username=(
                    "rifttrace-regression-admin"
                ),

                email=(
                    "regression@rifttrace.test"
                ),

                password=(
                    "Regression-Test-Password-123!"
                ),
            )
        )


        self.client.force_authenticate(
            user=(
                self.authenticated_test_user
            )
        )
