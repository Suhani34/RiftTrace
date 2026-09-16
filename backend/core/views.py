from django.http import JsonResponse


def health(request):
    return JsonResponse(
        {
            "status": "ok",
            "service": "rifttrace-backend",
            "message": "RiftTrace backend is running",
        }
    )
