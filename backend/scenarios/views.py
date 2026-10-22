from django.shortcuts import get_object_or_404

from rest_framework import (
    generics,
    status,
)

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    SavedScenario,
    ScenarioRun,
)

from .serializers import (
    SavedScenarioSerializer,
    ScenarioRunCreateSerializer,
    ScenarioRunSerializer,
)

from .services import (
    compare_scenario_runs,
    create_scenario_run,
)


class ScenarioListCreateView(
    generics.ListCreateAPIView
):
    serializer_class = (
        SavedScenarioSerializer
    )


    def get_queryset(
        self,
    ):
        queryset = (
            SavedScenario.objects
            .select_related(
                "organization"
            )
            .prefetch_related(
                "runs"
            )
        )


        organization_id = (
            self.request
            .query_params
            .get(
                "organization"
            )
        )

        simulation_type = (
            self.request
            .query_params
            .get(
                "simulation_type"
            )
        )


        if organization_id:
            queryset = queryset.filter(
                organization_id=(
                    organization_id
                )
            )


        if simulation_type:
            queryset = queryset.filter(
                simulation_type=(
                    simulation_type
                )
            )


        return queryset


class ScenarioDetailView(
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = (
        SavedScenarioSerializer
    )

    queryset = (
        SavedScenario.objects
        .select_related(
            "organization"
        )
        .prefetch_related(
            "runs"
        )
    )


class ScenarioRunListCreateView(
    APIView
):
    def get_scenario(
        self,
        scenario_id,
    ):
        return get_object_or_404(
            SavedScenario.objects
            .select_related(
                "organization"
            ),

            pk=scenario_id,
        )


    def get(
        self,
        request,
        scenario_id,
    ):
        scenario = self.get_scenario(
            scenario_id
        )

        runs = (
            scenario.runs
            .all()
        )


        serializer = (
            ScenarioRunSerializer(
                runs,
                many=True,
            )
        )


        return Response(
            serializer.data
        )


    def post(
        self,
        request,
        scenario_id,
    ):
        scenario = self.get_scenario(
            scenario_id
        )


        serializer = (
            ScenarioRunCreateSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )


        validated_data = (
            serializer.validated_data
        )


        request_payload = (
            validated_data.get(
                "request_payload",
                scenario.request_payload,
            )
        )


        run = create_scenario_run(
            scenario=scenario,

            request_payload=(
                request_payload
            ),

            result_payload=(
                validated_data.get(
                    "result_payload",
                    {},
                )
            ),

            metrics=(
                validated_data.get(
                    "metrics",
                    {},
                )
            ),

            status=(
                validated_data.get(
                    "status",
                    ScenarioRun.Status.SUCCESS,
                )
            ),

            label=(
                validated_data.get(
                    "label",
                    "",
                )
            ),

            error_message=(
                validated_data.get(
                    "error_message",
                    "",
                )
            ),
        )


        return Response(
            ScenarioRunSerializer(
                run
            ).data,

            status=(
                status.HTTP_201_CREATED
            ),
        )


class ScenarioCompareView(
    APIView
):
    def get(
        self,
        request,
        scenario_id,
    ):
        scenario = get_object_or_404(
            SavedScenario,

            pk=scenario_id,
        )


        before_run_id = (
            request
            .query_params
            .get(
                "before_run"
            )
        )

        after_run_id = (
            request
            .query_params
            .get(
                "after_run"
            )
        )


        if not before_run_id:
            return Response(
                {
                    "detail":
                        (
                            "before_run is required."
                        )
                },

                status=(
                    status.HTTP_400_BAD_REQUEST
                ),
            )


        if not after_run_id:
            return Response(
                {
                    "detail":
                        (
                            "after_run is required."
                        )
                },

                status=(
                    status.HTTP_400_BAD_REQUEST
                ),
            )


        before_run = get_object_or_404(
            ScenarioRun,

            pk=before_run_id,

            scenario=scenario,
        )

        after_run = get_object_or_404(
            ScenarioRun,

            pk=after_run_id,

            scenario=scenario,
        )


        try:
            metric_differences = (
                compare_scenario_runs(
                    before_run,
                    after_run,
                )
            )

        except ValueError as exc:
            return Response(
                {
                    "detail":
                        str(exc)
                },

                status=(
                    status.HTTP_400_BAD_REQUEST
                ),
            )


        return Response(
            {
                "scenario": {
                    "id":
                        scenario.id,

                    "name":
                        scenario.name,

                    "simulation_type":
                        scenario.simulation_type,
                },

                "before_run":
                    ScenarioRunSerializer(
                        before_run
                    ).data,

                "after_run":
                    ScenarioRunSerializer(
                        after_run
                    ).data,

                "metrics":
                    metric_differences,

                "disclaimer":
                    (
                        "This comparison describes "
                        "differences between modeled "
                        "simulation runs. It does not "
                        "claim observed real-world "
                        "attack behavior."
                    ),
            }
        )
