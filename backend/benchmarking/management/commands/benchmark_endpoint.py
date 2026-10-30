import cProfile
import gc
import hashlib
import json
import math
import statistics
import time
import tracemalloc

from pathlib import Path

from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from django.db import connection

from django.test import (
    Client,
    override_settings,
)

from django.test.utils import (
    CaptureQueriesContext,
)

from benchmarking.models import (
    BenchmarkResult,
)

from organizations.models import (
    Organization,
)


class Command(BaseCommand):
    help = (
        "Benchmark an existing RiftTrace "
        "API endpoint."
    )


    def add_arguments(
        self,
        parser,
    ):
        parser.add_argument(
            "--name",
            required=True,
        )

        parser.add_argument(
            "--variant",
            choices=(
                "BASELINE",
                "OPTIMIZED",
            ),
            required=True,
        )

        parser.add_argument(
            "--endpoint",
            required=True,
        )

        parser.add_argument(
            "--method",
            choices=(
                "GET",
                "POST",
            ),
            default="POST",
        )

        parser.add_argument(
            "--payload",
            required=False,
        )

        parser.add_argument(
            "--organization",
            type=int,
            required=False,
        )

        parser.add_argument(
            "--asset-count",
            type=int,
            default=0,
        )

        parser.add_argument(
            "--relationship-count",
            type=int,
            default=0,
        )

        parser.add_argument(
            "--iterations",
            type=int,
            default=10,
        )

        parser.add_argument(
            "--warmups",
            type=int,
            default=2,
        )

        parser.add_argument(
            "--profile-output",
            required=False,
        )

        parser.add_argument(
            "--notes",
            default="",
        )


    def handle(
        self,
        *args,
        **options,
    ):
        method = (
            options[
                "method"
            ]
        )

        endpoint = (
            options[
                "endpoint"
            ]
        )

        iterations = (
            options[
                "iterations"
            ]
        )

        warmups = (
            options[
                "warmups"
            ]
        )


        if iterations < 1:
            raise CommandError(
                "iterations must be at least 1."
            )


        if warmups < 0:
            raise CommandError(
                "warmups cannot be negative."
            )


        payload = None
        payload_sha256 = ""


        payload_path = (
            options.get(
                "payload"
            )
        )


        if payload_path:
            raw_payload = (
                Path(
                    payload_path
                )
                .read_bytes()
            )

            payload_sha256 = (
                hashlib.sha256(
                    raw_payload
                )
                .hexdigest()
            )


            try:
                payload = json.loads(
                    raw_payload
                    .decode(
                        "utf-8"
                    )
                )

            except json.JSONDecodeError as exc:
                raise CommandError(
                    (
                        "Payload file is not "
                        f"valid JSON: {exc}"
                    )
                ) from exc


        if (
            method == "POST"
            and payload is None
        ):
            raise CommandError(
                (
                    "POST benchmarks require "
                    "--payload."
                )
            )


        organization = None


        organization_id = (
            options.get(
                "organization"
            )
        )


        if organization_id:
            try:
                organization = (
                    Organization.objects
                    .get(
                        pk=organization_id
                    )
                )

            except Organization.DoesNotExist as exc:
                raise CommandError(
                    (
                        "Organization does "
                        "not exist."
                    )
                ) from exc


        client = Client()


        def perform_request():
            if method == "GET":
                return client.get(
                    endpoint
                )


            return client.post(
                endpoint,

                data=json.dumps(
                    payload
                ),

                content_type=(
                    "application/json"
                ),
            )


        with override_settings(
            ALLOWED_HOSTS=[
                "testserver",
                "127.0.0.1",
                "localhost",
            ]
        ):
            self.stdout.write(
                (
                    f"Warm-up requests: "
                    f"{warmups}"
                )
            )


            for _ in range(
                warmups
            ):
                response = (
                    perform_request()
                )


                if not (
                    200
                    <= response.status_code
                    < 300
                ):
                    raise CommandError(
                        (
                            "Warm-up request "
                            "failed with HTTP "
                            f"{response.status_code}: "
                            f"{response.content[:500]!r}"
                        )
                    )


            samples = []
            status_code = 0


            for iteration in range(
                1,
                iterations + 1,
            ):
                gc.collect()


                with CaptureQueriesContext(
                    connection
                ) as query_context:
                    tracemalloc.start()

                    start = (
                        time.perf_counter()
                    )


                    response = (
                        perform_request()
                    )


                    elapsed_ms = (
                        (
                            time.perf_counter()
                            - start
                        )
                        * 1000
                    )


                    (
                        _current_memory,
                        peak_memory,
                    ) = (
                        tracemalloc
                        .get_traced_memory()
                    )

                    tracemalloc.stop()


                status_code = (
                    response.status_code
                )


                if not (
                    200
                    <= status_code
                    < 300
                ):
                    raise CommandError(
                        (
                            f"Iteration "
                            f"{iteration} failed "
                            f"with HTTP "
                            f"{status_code}: "
                            f"{response.content[:500]!r}"
                        )
                    )


                sample = {
                    "iteration":
                        iteration,

                    "elapsed_ms":
                        round(
                            elapsed_ms,
                            3,
                        ),

                    "query_count":
                        len(
                            query_context
                        ),

                    "peak_memory_kib":
                        round(
                            (
                                peak_memory
                                / 1024
                            ),
                            3,
                        ),
                }


                samples.append(
                    sample
                )


                self.stdout.write(
                    (
                        f"Iteration "
                        f"{iteration}: "
                        f"{elapsed_ms:.2f} ms, "
                        f"{len(query_context)} "
                        f"queries"
                    )
                )


            elapsed_values = [
                sample[
                    "elapsed_ms"
                ]

                for sample
                in samples
            ]

            query_values = [
                sample[
                    "query_count"
                ]

                for sample
                in samples
            ]

            memory_values = [
                sample[
                    "peak_memory_kib"
                ]

                for sample
                in samples
            ]


            sorted_elapsed = sorted(
                elapsed_values
            )


            p95_index = max(
                0,

                math.ceil(
                    len(
                        sorted_elapsed
                    )
                    * 0.95
                )
                - 1,
            )


            result = (
                BenchmarkResult.objects
                .create(
                    name=(
                        options[
                            "name"
                        ]
                    ),

                    variant=(
                        options[
                            "variant"
                        ]
                    ),

                    organization=(
                        organization
                    ),

                    endpoint=(
                        endpoint
                    ),

                    method=(
                        method
                    ),

                    asset_count=(
                        options[
                            "asset_count"
                        ]
                    ),

                    relationship_count=(
                        options[
                            "relationship_count"
                        ]
                    ),

                    iterations=(
                        iterations
                    ),

                    warmup_iterations=(
                        warmups
                    ),

                    mean_ms=round(
                        statistics.mean(
                            elapsed_values
                        ),
                        3,
                    ),

                    median_ms=round(
                        statistics.median(
                            elapsed_values
                        ),
                        3,
                    ),

                    p95_ms=round(
                        sorted_elapsed[
                            p95_index
                        ],
                        3,
                    ),

                    min_ms=round(
                        min(
                            elapsed_values
                        ),
                        3,
                    ),

                    max_ms=round(
                        max(
                            elapsed_values
                        ),
                        3,
                    ),

                    peak_memory_kib=round(
                        max(
                            memory_values
                        ),
                        3,
                    ),

                    mean_query_count=round(
                        statistics.mean(
                            query_values
                        ),
                        3,
                    ),

                    status_code=(
                        status_code
                    ),

                    payload_sha256=(
                        payload_sha256
                    ),

                    samples=(
                        samples
                    ),

                    notes=(
                        options[
                            "notes"
                        ]
                    ),
                )
            )


            profile_output = (
                options.get(
                    "profile_output"
                )
            )


            if profile_output:
                profile_path = Path(
                    profile_output
                )

                profile_path.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )


                profiler = (
                    cProfile.Profile()
                )

                profiler.enable()

                profile_response = (
                    perform_request()
                )

                profiler.disable()


                if not (
                    200
                    <= profile_response.status_code
                    < 300
                ):
                    raise CommandError(
                        (
                            "Profile request "
                            "failed."
                        )
                    )


                profiler.dump_stats(
                    profile_path
                )


                self.stdout.write(
                    (
                        "Profile written to "
                        f"{profile_path}"
                    )
                )


        self.stdout.write("")


        self.stdout.write(
            self.style.SUCCESS(
                (
                    f"Benchmark #{result.id}"
                    f" saved."
                )
            )
        )


        self.stdout.write(
            (
                f"Mean: "
                f"{result.mean_ms:.2f} ms"
            )
        )

        self.stdout.write(
            (
                f"Median: "
                f"{result.median_ms:.2f} ms"
            )
        )

        self.stdout.write(
            (
                f"P95: "
                f"{result.p95_ms:.2f} ms"
            )
        )

        self.stdout.write(
            (
                f"Peak Python allocation: "
                f"{result.peak_memory_kib:.2f} KiB"
            )
        )

        self.stdout.write(
            (
                f"Mean SQL queries: "
                f"{result.mean_query_count:.2f}"
            )
        )
