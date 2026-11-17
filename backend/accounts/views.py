from django.contrib.auth import (
    authenticate,
    login,
    logout,
)

from django.utils.decorators import (
    method_decorator,
)

from django.views.decorators.csrf import (
    csrf_protect,
    ensure_csrf_cookie,
)

from rest_framework import status

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)

from rest_framework.response import (
    Response,
)

from rest_framework.views import (
    APIView,
)

from .serializers import (
    LoginSerializer,
)

from .throttles import (
    LoginRateThrottle,
)


@method_decorator(
    ensure_csrf_cookie,
    name="dispatch",
)
class CsrfView(
    APIView
):
    permission_classes = [
        AllowAny
    ]


    def get(
        self,
        request,
    ):
        return Response(
            {
                "detail":
                    "CSRF cookie set."
            }
        )


@method_decorator(
    csrf_protect,
    name="dispatch",
)
class LoginView(
    APIView
):
    permission_classes = [
        AllowAny
    ]

    throttle_classes = [
        LoginRateThrottle
    ]


    def post(
        self,
        request,
    ):
        serializer = (
            LoginSerializer(
                data=request.data
            )
        )


        serializer.is_valid(
            raise_exception=True
        )


        user = authenticate(
            request=request,

            username=(
                serializer
                .validated_data[
                    "username"
                ]
            ),

            password=(
                serializer
                .validated_data[
                    "password"
                ]
            ),
        )


        if user is None:
            return Response(
                {
                    "detail":
                        (
                            "Invalid username "
                            "or password."
                        )
                },

                status=(
                    status
                    .HTTP_400_BAD_REQUEST
                ),
            )


        if not user.is_active:
            return Response(
                {
                    "detail":
                        (
                            "This account "
                            "is disabled."
                        )
                },

                status=(
                    status
                    .HTTP_403_FORBIDDEN
                ),
            )


        login(
            request,
            user,
        )


        return Response(
            {
                "id":
                    user.id,

                "username":
                    user.username,

                "is_superuser":
                    user.is_superuser,
            }
        )


class LogoutView(
    APIView
):
    permission_classes = [
        IsAuthenticated
    ]


    def post(
        self,
        request,
    ):
        logout(
            request
        )


        return Response(
            {
                "detail":
                    "Logged out."
            }
        )


class MeView(
    APIView
):
    permission_classes = [
        IsAuthenticated
    ]


    def get(
        self,
        request,
    ):
        user = (
            request.user
        )


        memberships = (
            user
            .organization_memberships
            .select_related(
                "organization"
            )
            .order_by(
                "organization__name"
            )
        )


        return Response(
            {
                "id":
                    user.id,

                "username":
                    user.username,

                "email":
                    user.email,

                "is_superuser":
                    user.is_superuser,

                "memberships": [
                    {
                        "organization_id":
                            membership
                            .organization_id,

                        "organization_name":
                            membership
                            .organization
                            .name,

                        "role":
                            membership.role,
                    }

                    for membership
                    in memberships
                ],
            }
        )
