from django.urls import include, path
from rest_framework.routers import DefaultRouter

from assets.views import (
    AssetViewSet,
    NetworkZoneViewSet,
    RelationshipViewSet,
)
from organizations.views import OrganizationViewSet


router = DefaultRouter()

router.register(
    "zones",
    NetworkZoneViewSet,
    basename="zone",
)

router.register(
    "organizations",
    OrganizationViewSet,
    basename="organization",
)

router.register(
    "assets",
    AssetViewSet,
    basename="asset",
)

router.register(
    "relationships",
    RelationshipViewSet,
    basename="relationship",
)


urlpatterns = [
    path("", include("core.urls")),
    path("", include(router.urls)),
    path("simulations/", include("simulations.urls")),
]
