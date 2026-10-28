import csv

from django.http import HttpResponse

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    EvaluationExperiment,
)

from .serializers import (
    EvaluationExperimentSerializer,
)

from .services import (
    build_evaluation_rows,
    build_evaluation_summary,
)


def evaluation_queryset():
    return (
        EvaluationExperiment.objects
        .select_related(
            "organization",
            "scenario",
            "baseline_run",
            "treatment_run",
        )
    )


class EvaluationExperimentListCreateView(
    generics.ListCreateAPIView
):
    serializer_class = (
        EvaluationExperimentSerializer
    )


    def get_queryset(
        self,
    ):
        queryset = (
            evaluation_queryset()
        )


        organization_id = (
            self.request
            .query_params
            .get(
                "organization"
            )
        )


        if organization_id:
            queryset = queryset.filter(
                organization_id=(
                    organization_id
                )
            )


        return queryset


class EvaluationExperimentDetailView(
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = (
        EvaluationExperimentSerializer
    )

    queryset = (
        evaluation_queryset()
    )


class EvaluationSummaryView(
    APIView
):
    def get(
        self,
        request,
    ):
        queryset = (
            evaluation_queryset()
        )


        organization_id = (
            request
            .query_params
            .get(
                "organization"
            )
        )


        if organization_id:
            queryset = queryset.filter(
                organization_id=(
                    organization_id
                )
            )


        return Response(
            build_evaluation_summary(
                queryset
            )
        )


class EvaluationCsvExportView(
    APIView
):
    def get(
        self,
        request,
    ):
        queryset = (
            evaluation_queryset()
        )


        organization_id = (
            request
            .query_params
            .get(
                "organization"
            )
        )


        if organization_id:
            queryset = queryset.filter(
                organization_id=(
                    organization_id
                )
            )


        rows = (
            build_evaluation_rows(
                queryset
            )
        )


        response = HttpResponse(
            content_type=(
                "text/csv"
            )
        )

        response[
            "Content-Disposition"
        ] = (
            'attachment; '
            'filename="rifttrace_evaluation.csv"'
        )


        fieldnames = [
            "experiment_id",
            "experiment_name",
            "organization",
            "scenario",
            "simulation_type",
            "intervention",
            "baseline_run",
            "treatment_run",
            "metric",
            "metric_label",
            "before",
            "after",
            "reduction",
            "interpretation",
        ]


        writer = csv.DictWriter(
            response,
            fieldnames=fieldnames,
        )

        writer.writeheader()


        for row in rows:
            writer.writerow(
                row
            )


        return response
