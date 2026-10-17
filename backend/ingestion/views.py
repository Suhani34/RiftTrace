from rest_framework import (
    status,
)

from rest_framework.response import (
    Response,
)

from rest_framework.views import (
    APIView,
)

from .models import (
    IngestionRun,
)

from .serializers import (
    IngestionRunSerializer,
    IngestionUploadSerializer,
)

from .services.applier import (
    InvalidIngestionPlan,
    apply_ingestion_bundle,
)

from .services.parsers import (
    IngestionParseError,
    parse_ingestion_upload,
)

from .services.planner import (
    build_ingestion_plan,
)


class IngestionPreviewView(
    APIView
):
    def post(self, request):
        serializer = (
            IngestionUploadSerializer(
                data=request.data
            )
        )


        serializer.is_valid(
            raise_exception=True
        )


        organization = (
            serializer.validated_data[
                "organization"
            ]
        )


        try:
            bundle = (
                parse_ingestion_upload(
                    serializer
                    .validated_data
                )
            )

        except IngestionParseError as exc:
            return Response(
                {
                    "valid": False,

                    "parse_error":
                        str(
                            exc
                        ),

                    "issues": [
                        {
                            "section":
                                "parser",

                            "message":
                                str(
                                    exc
                                ),
                        }
                    ],
                },

                status=(
                    status
                    .HTTP_400_BAD_REQUEST
                ),
            )


        plan = build_ingestion_plan(
            organization,
            bundle,
        )


        return Response(
            plan,

            status=status.HTTP_200_OK,
        )


class IngestionApplyView(
    APIView
):
    def post(self, request):
        serializer = (
            IngestionUploadSerializer(
                data=request.data
            )
        )


        serializer.is_valid(
            raise_exception=True
        )


        organization = (
            serializer.validated_data[
                "organization"
            ]
        )


        source_format = (
            serializer.validated_data[
                "source_format"
            ]
        )


        try:
            bundle = (
                parse_ingestion_upload(
                    serializer
                    .validated_data
                )
            )


            (
                run,
                plan,
            ) = apply_ingestion_bundle(
                organization=organization,

                source_format=(
                    source_format
                ),

                bundle=bundle,
            )


        except IngestionParseError as exc:
            return Response(
                {
                    "detail":
                        str(
                            exc
                        )
                },

                status=(
                    status
                    .HTTP_400_BAD_REQUEST
                ),
            )


        except InvalidIngestionPlan as exc:
            return Response(
                exc.plan,

                status=(
                    status
                    .HTTP_400_BAD_REQUEST
                ),
            )


        return Response(
            {
                "applied": True,

                "run":
                    IngestionRunSerializer(
                        run
                    ).data,

                "plan":
                    plan,
            },

            status=(
                status
                .HTTP_201_CREATED
            ),
        )


class IngestionRunListView(
    APIView
):
    def get(self, request):
        organization_id = (
            request.query_params.get(
                "organization"
            )
        )


        queryset = (
            IngestionRun.objects
            .select_related(
                "organization"
            )
            .all()
        )


        if organization_id:
            queryset = (
                queryset.filter(
                    organization_id=(
                        organization_id
                    )
                )
            )


        queryset = queryset[:20]


        return Response(
            IngestionRunSerializer(
                queryset,

                many=True,
            ).data
        )
