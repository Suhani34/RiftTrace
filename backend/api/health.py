import logging

from django.db import (
    connection,
)

from rest_framework import (
    status,
)

from rest_framework.permissions import (
    AllowAny,
)

from rest_framework.response import (
    Response,
)

from rest_framework.views import (
    APIView,
)


LOGGER = logging.getLogger(
    "rifttrace.health"
)


class LivenessView(
    APIView
):
    authentication_classes = []

    permission_classes = [
        AllowAny
    ]

    throttle_classes = []

    def get(
        self,
        request,
    ):
        return Response(
            {
                "status": "ok",
            }
        )


class ReadinessView(
    APIView
):
    authentication_classes = []

    permission_classes = [
        AllowAny
    ]

    throttle_classes = []

    def get(
        self,
        request,
    ):
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT 1"
                )

                cursor.fetchone()

        except Exception:
            LOGGER.exception(
                (
                    "Database readiness "
                    "check failed."
                )
            )

            return Response(
                {
                    "status":
                        "unavailable",

                    "database":
                        "unavailable",
                },
                status=(
                    status
                    .HTTP_503_SERVICE_UNAVAILABLE
                ),
            )

        return Response(
            {
                "status": "ok",
                "database": "ok",
            }
        )
