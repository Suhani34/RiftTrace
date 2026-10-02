from django.urls import include, path
from rest_framework.routers import DefaultRouter
from security.views import (
    VulnerabilityViewSet,
)
from assets.views import (
    AssetViewSet,
    NetworkZoneViewSet,
    RelationshipViewSet,
)
from business.views import (
    BusinessProcessDependencyViewSet,
    BusinessProcessViewSet,
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
    "business-processes",
    BusinessProcessViewSet,
    basename="business-process",
)

router.register(
    "business-dependencies",
    BusinessProcessDependencyViewSet,
    basename="business-dependency",
)

router.register(
    "vulnerabilities",
    VulnerabilityViewSet,
    basename="vulnerability",
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
