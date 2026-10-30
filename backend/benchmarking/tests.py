from rest_framework import status
from rest_framework.test import APITestCase

from benchmarking.models import (
    BenchmarkResult,
)


class BenchmarkingApiTests(
    APITestCase
):
    def test_empty_result_list(
        self,
    ):
        response = self.client.get(
            "/api/benchmarking/results/"
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


    def test_result_is_returned(
        self,
    ):
        BenchmarkResult.objects.create(
            name=(
                "reachability-scale"
            ),

            variant=(
                BenchmarkResult
                .Variant
                .BASELINE
            ),

            endpoint=(
                "/api/simulations/"
                "reachability/"
            ),

            method="POST",

            asset_count=100,

            relationship_count=99,

            iterations=10,

            warmup_iterations=2,

            mean_ms=120.0,

            median_ms=118.0,

            p95_ms=145.0,

            min_ms=110.0,

            max_ms=150.0,

            peak_memory_kib=2048.0,

            mean_query_count=8.0,

            status_code=200,

            samples=[],
        )


        response = self.client.get(
            "/api/benchmarking/results/"
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


        self.assertEqual(
            len(
                response.data
            ),
            1,
        )


        self.assertEqual(
            response.data[
                0
            ][
                "asset_count"
            ],
            100,
        )
