from rest_framework import viewsets

from .models import (
    BusinessProcess,
    BusinessProcessDependency,
)

from .serializers import (
    BusinessProcessDependencySerializer,
    BusinessProcessSerializer,
)


class BusinessProcessViewSet(
    viewsets.ModelViewSet
):
    serializer_class = (
        BusinessProcessSerializer
    )

    queryset = (
        BusinessProcess.objects
        .select_related(
            "organization",
        )
        .all()
    )

    def get_queryset(self):
        queryset = super().get_queryset()

        organization = (
            self.request
            .query_params
            .get("organization")
        )

        criticality = (
            self.request
            .query_params
            .get("criticality")
        )

        if organization:
            queryset = queryset.filter(
                organization_id=(
                    organization
                )
            )

        if criticality:
            queryset = queryset.filter(
                criticality=criticality
            )

        return queryset


class BusinessProcessDependencyViewSet(
    viewsets.ModelViewSet
):
    serializer_class = (
        BusinessProcessDependencySerializer
    )

    queryset = (
        BusinessProcessDependency.objects
        .select_related(
            "business_process",
            (
                "business_process"
                "__organization"
            ),
            "asset",
        )
        .all()
    )

    def get_queryset(self):
        queryset = super().get_queryset()

        organization = (
            self.request
            .query_params
            .get("organization")
        )

        business_process = (
            self.request
            .query_params
            .get(
                "business_process"
            )
        )

        asset = (
            self.request
            .query_params
            .get("asset")
        )

        if organization:
            queryset = queryset.filter(
                business_process__organization_id=(
                    organization
                )
            )

        if business_process:
            queryset = queryset.filter(
                business_process_id=(
                    business_process
                )
            )

        if asset:
            queryset = queryset.filter(
                asset_id=asset
            )

        return queryset
