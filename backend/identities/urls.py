from rest_framework.routers import (
    DefaultRouter,
)

from .views import (
    CredentialExposureViewSet,
    IdentityAccessViewSet,
    IdentityLinkViewSet,
    IdentityViewSet,
)


router = DefaultRouter()

router.register(
    "identities",
    IdentityViewSet,
    basename="identity",
)

router.register(
    "credential-exposures",
    CredentialExposureViewSet,
    basename="credential-exposure",
)

router.register(
    "identity-access",
    IdentityAccessViewSet,
    basename="identity-access",
)

router.register(
    "identity-links",
    IdentityLinkViewSet,
    basename="identity-link",
)


urlpatterns = router.urls
