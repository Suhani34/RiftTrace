from rest_framework.views import (
    exception_handler,
)


def rifttrace_exception_handler(
    exc,
    context,
):
    """
    RiftTrace API exception handler.

    DRF keeps its normal validation/error
    structure, while RiftTrace adds the
    HTTP status code consistently.

    Unexpected Python exceptions are not
    hidden here. If DRF cannot handle an
    exception, None is returned and Django
    treats it as a real server error.
    """

    response = exception_handler(
        exc,
        context,
    )


    if response is None:
        return None


    original_data = (
        response.data
    )


    if isinstance(
        original_data,
        dict,
    ):
        response.data = {
            "status_code":
                response.status_code,

            **original_data,
        }

    else:
        response.data = {
            "status_code":
                response.status_code,

            "detail":
                original_data,
        }


    return response
