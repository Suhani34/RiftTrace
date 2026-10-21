from rest_framework import (
    status,
    viewsets,
)

from rest_framework.response import (
    Response,
)

from rest_framework.views import (
    APIView,
)

from .models import (
    AttackMappingRule,
    AttackTechnique,
)

from .serializers import (
    AttackMappingEvaluateSerializer,
    AttackMappingRuleSerializer,
    AttackTechniqueSerializer,
)

from .services import (
    load_attack_mapping_context,
    map_attack_event,
)


class AttackTechniqueViewSet(
    viewsets.ReadOnlyModelViewSet
):
    serializer_class = (
        AttackTechniqueSerializer
    )


    queryset = (
        AttackTechnique
        .objects
        .filter(
            enabled=True
        )
        .order_by(
            "attack_id"
        )
    )


class AttackMappingRuleViewSet(
    viewsets.ReadOnlyModelViewSet
):
    serializer_class = (
        AttackMappingRuleSerializer
    )


    queryset = (
        AttackMappingRule
        .objects
        .filter(
            enabled=True
        )
        .select_related(
            "technique"
        )
        .order_by(
            "priority",
            "rule_code",
        )
    )


class AttackMappingEvaluateView(
    APIView
):
    def post(
        self,
        request,
    ):
        serializer = (
            AttackMappingEvaluateSerializer(
                data=request.data
            )
        )


        serializer.is_valid(
            raise_exception=True
        )


        event_type = (
            serializer
            .validated_data[
                "event_type"
            ]
        )


        attributes = (
            serializer
            .validated_data[
                "attributes"
            ]
        )


        context = (
            load_attack_mapping_context()
        )


        annotations = (
            map_attack_event(
                event_type=event_type,

                attributes=attributes,

                context=context,
            )
        )


        return Response(
            {
                "event_type":
                    event_type,

                "attributes":
                    attributes,

                "annotations":
                    annotations,

                "disclaimer":
                    (
                        "ATT&CK annotations "
                        "describe modeled "
                        "behavior consistent "
                        "with mapping rules; "
                        "they are not detections "
                        "or evidence that an "
                        "attack occurred."
                    ),
            },

            status=status.HTTP_200_OK,
        )
