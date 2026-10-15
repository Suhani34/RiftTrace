from django.shortcuts import (
    get_object_or_404,
)

from rest_framework import status
from rest_framework.response import (
    Response,
)
from rest_framework.views import (
    APIView,
)

from assets.models import (
    Asset,
    NetworkZone,
    Relationship,
)

from business.models import (
    BusinessProcess,
    BusinessProcessDependency,
)

from organizations.models import (
    Organization,
)

from organizations.serializers import (
    OrganizationSerializer,
)

from security.models import (
    SecurityControl,
    Vulnerability,
)


class DashboardSummaryView(APIView):
    def get(self, request):
        organization_id = (
            request.query_params.get(
                "organization"
            )
        )


        if not organization_id:
            return Response(
                {
                    "detail": (
                        "organization query "
                        "parameter is required."
                    )
                },

                status=(
                    status
                    .HTTP_400_BAD_REQUEST
                ),
            )


        organization = (
            get_object_or_404(
                Organization,

                id=organization_id,
            )
        )


        assets = Asset.objects.filter(
            organization=organization
        )


        relationships = (
            Relationship.objects.filter(
                source__organization=(
                    organization
                ),

                target__organization=(
                    organization
                ),
            )
        )


        vulnerabilities = (
            Vulnerability.objects.filter(
                asset__organization=(
                    organization
                )
            )
        )


        controls = (
            SecurityControl.objects.filter(
                organization=organization
            )
        )


        processes = (
            BusinessProcess.objects.filter(
                organization=organization
            )
        )


        dependencies = (
            BusinessProcessDependency
            .objects
            .filter(
                business_process__organization=(
                    organization
                )
            )
        )


        asset_criticality = [
            {
                "name": label,

                "key": value,

                "value": (
                    assets.filter(
                        criticality=value
                    ).count()
                ),
            }

            for value, label
            in Asset.Criticality.choices
        ]


        process_criticality = [
            {
                "name": label,

                "key": value,

                "value": (
                    processes.filter(
                        criticality=value
                    ).count()
                ),
            }

            for value, label
            in (
                BusinessProcess
                .Criticality
                .choices
            )
        ]


        control_types = [
            {
                "name": label,

                "key": value,

                "value": (
                    controls.filter(
                        control_type=value
                    ).count()
                ),
            }

            for value, label
            in (
                SecurityControl
                .ControlType
                .choices
            )
        ]


        return Response(
            {
                "organization":
                    OrganizationSerializer(
                        organization
                    ).data,

                "totals": {
                    "network_zones":
                        NetworkZone
                        .objects
                        .filter(
                            organization=(
                                organization
                            )
                        )
                        .count(),

                    "assets":
                        assets.count(),

                    "relationships":
                        relationships.count(),

                    "vulnerabilities":
                        vulnerabilities.count(),

                    "exploitable_vulnerabilities":
                        vulnerabilities
                        .filter(
                            is_exploitable=True
                        )
                        .count(),

                    "security_controls":
                        controls.count(),

                    "business_processes":
                        processes.count(),

                    "business_dependencies":
                        dependencies.count(),
                },

                "asset_criticality":
                    asset_criticality,

                "business_process_criticality":
                    process_criticality,

                "security_control_types":
                    control_types,
            }
        )
