import json
import logging
import re
import uuid

from datetime import (
    datetime,
    timezone,
)

from time import (
    perf_counter,
)


REQUEST_ID_PATTERN = re.compile(
    r"^[A-Za-z0-9._:-]{1,128}$"
)


REQUEST_LOGGER = logging.getLogger(
    "rifttrace.request"
)


HEALTH_PATHS = {
    "/api/health/live/",
    "/api/health/ready/",
}


class JsonFormatter(
    logging.Formatter
):
    EXTRA_FIELDS = (
        "request_id",
        "method",
        "path",
        "status_code",
        "duration_ms",
    )

    def format(
        self,
        record,
    ):
        payload = {
            "timestamp": (
                datetime.now(
                    timezone.utc
                ).isoformat()
            ),
            "level": (
                record.levelname
            ),
            "logger": (
                record.name
            ),
            "message": (
                record.getMessage()
            ),
        }

        for field in self.EXTRA_FIELDS:
            value = getattr(
                record,
                field,
                None,
            )

            if value is not None:
                payload[field] = value

        if record.exc_info:
            payload["exception"] = (
                self.formatException(
                    record.exc_info
                )
            )

        return json.dumps(
            payload,
            default=str,
        )


def get_request_id(
    request,
):
    supplied_request_id = (
        request.headers.get(
            "X-Request-ID",
            "",
        ).strip()
    )

    if REQUEST_ID_PATTERN.fullmatch(
        supplied_request_id
    ):
        return supplied_request_id

    return str(
        uuid.uuid4()
    )


class RequestLoggingMiddleware:
    def __init__(
        self,
        get_response,
    ):
        self.get_response = (
            get_response
        )

    def __call__(
        self,
        request,
    ):
        request_id = get_request_id(
            request
        )

        request.request_id = (
            request_id
        )

        started_at = perf_counter()

        try:
            response = (
                self.get_response(
                    request
                )
            )
        except Exception:
            duration_ms = round(
                (
                    perf_counter()
                    - started_at
                )
                * 1000,
                2,
            )

            REQUEST_LOGGER.exception(
                "request_failed",
                extra={
                    "request_id": (
                        request_id
                    ),
                    "method": (
                        request.method
                    ),
                    "path": (
                        request.path
                    ),
                    "duration_ms": (
                        duration_ms
                    ),
                },
            )

            raise

        duration_ms = round(
            (
                perf_counter()
                - started_at
            )
            * 1000,
            2,
        )

        response[
            "X-Request-ID"
        ] = request_id

        should_log = (
            request.path
            not in HEALTH_PATHS
            or response.status_code
            >= 400
        )

        if should_log:
            if response.status_code >= 500:
                log_level = (
                    logging.ERROR
                )
            elif response.status_code >= 400:
                log_level = (
                    logging.WARNING
                )
            else:
                log_level = (
                    logging.INFO
                )

            REQUEST_LOGGER.log(
                log_level,
                "request_completed",
                extra={
                    "request_id": (
                        request_id
                    ),
                    "method": (
                        request.method
                    ),
                    "path": (
                        request.path
                    ),
                    "status_code": (
                        response.status_code
                    ),
                    "duration_ms": (
                        duration_ms
                    ),
                },
            )

        return response
