from rest_framework import viewsets

from .models import (
    CredentialExposure,
    Identity,
    IdentityAccess,
    IdentityLink,
)

from .serializers import (
    CredentialExposureSerializer,
    IdentityAccessSerializer,
    IdentityLinkSerializer,
    IdentitySerializer,
)


class OrganizationFilteredViewSet(
    viewsets.ModelViewSet
):
    def filter_organization(
        self,
        queryset,
    ):
        organization_id = (
            self.request.query_params.get(
                "organization"
            )
        )


        if organization_id:
            queryset = queryset.filter(
                organization_id=(
                    organization_id
                )
            )


        return queryset


class IdentityViewSet(
    OrganizationFilteredViewSet
):
    serializer_class = IdentitySerializer


    def get_queryset(self):
        return self.filter_organization(
            Identity.objects.all()
        )


class CredentialExposureViewSet(
    OrganizationFilteredViewSet
):
    serializer_class = (
        CredentialExposureSerializer
    )


    def get_queryset(self):
        return self.filter_organization(
            CredentialExposure.objects
            .select_related(
                "organization",
                "identity",
                "stored_on_asset",
            )
        )


class IdentityAccessViewSet(
    OrganizationFilteredViewSet
):
    serializer_class = (
        IdentityAccessSerializer
    )


    def get_queryset(self):
        return self.filter_organization(
            IdentityAccess.objects
            .select_related(
                "organization",
                "identity",
                "asset",
            )
        )


class IdentityLinkViewSet(
    OrganizationFilteredViewSet
):
    serializer_class = (
        IdentityLinkSerializer
    )


    def get_queryset(self):
        return self.filter_organization(
            IdentityLink.objects
            .select_related(
                "organization",
                "source_identity",
                "target_identity",
            )
        )
