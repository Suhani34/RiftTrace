from rest_framework import generics

from .models import BenchmarkResult
from .serializers import BenchmarkResultSerializer


class BenchmarkResultListView(
    generics.ListAPIView
):
    serializer_class = (
        BenchmarkResultSerializer
    )


    def get_queryset(
        self,
    ):
        queryset = (
            BenchmarkResult.objects
            .select_related(
                "organization"
            )
        )


        name = (
            self.request
            .query_params
            .get(
                "name"
            )
        )

        organization_id = (
            self.request
            .query_params
            .get(
                "organization"
            )
        )


        if name:
            queryset = queryset.filter(
                name=name
            )


        if organization_id:
            queryset = queryset.filter(
                organization_id=(
                    organization_id
                )
            )


        return queryset
