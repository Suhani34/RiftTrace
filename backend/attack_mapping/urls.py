from django.urls import path

from rest_framework.routers import (
    DefaultRouter,
)

from .views import (
    AttackMappingEvaluateView,
    AttackMappingRuleViewSet,
    AttackTechniqueViewSet,
)


router = DefaultRouter()


router.register(
    "techniques",

    AttackTechniqueViewSet,

    basename="attack-technique",
)


router.register(
    "rules",

    AttackMappingRuleViewSet,

    basename="attack-mapping-rule",
)


urlpatterns = [
    path(
        "evaluate/",

        AttackMappingEvaluateView.as_view(),

        name="attack-mapping-evaluate",
    ),
]


urlpatterns += router.urls
