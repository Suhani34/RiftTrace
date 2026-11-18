from django.urls import (
    reverse,
)

from rest_framework import (
    status,
)

from rest_framework.test import (
    APITestCase,
)

from accounts.testing import (
    AuthenticatedAPITestCase,
)


class ApiExceptionFormatTests(
    AuthenticatedAPITestCase
):
    def test_missing_organization_has_status_code(
        self,
    ):
        response = self.client.get(
            reverse(
                "dashboard-summary"
            )
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )


        self.assertEqual(
            response.data[
                "status_code"
            ],
            400,
        )


        self.assertIn(
            "detail",
            response.data,
        )


    def test_unknown_organization_has_status_code(
        self,
    ):
        response = self.client.get(
            reverse(
                "dashboard-summary"
            ),

            {
                "organization":
                    999999999,
            },
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )


        self.assertEqual(
            response.data[
                "status_code"
            ],
            404,
        )


        self.assertIn(
            "detail",
            response.data,
        )


class UnauthenticatedApiExceptionTests(
    APITestCase
):
    def test_unauthenticated_request_has_status_code(
        self,
    ):
        response = self.client.get(
            reverse(
                "dashboard-summary"
            ),

            {
                "organization": 1,
            },
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )


        self.assertEqual(
            response.data[
                "status_code"
            ],
            403,
        )
