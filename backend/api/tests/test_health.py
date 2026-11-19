from django.urls import (
    reverse,
)

from rest_framework import (
    status,
)

from rest_framework.test import (
    APITestCase,
)


class HealthEndpointTests(
    APITestCase
):
    def test_liveness_is_public(
        self,
    ):
        response = self.client.get(
            reverse(
                "health-live"
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data,
            {
                "status": "ok",
            },
        )


    def test_readiness_is_public(
        self,
    ):
        response = self.client.get(
            reverse(
                "health-ready"
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data,
            {
                "status": "ok",
                "database": "ok",
            },
        )
