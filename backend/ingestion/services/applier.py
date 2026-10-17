from django.db import (
    transaction,
)

from assets.models import (
    Asset,
    NetworkZone,
    Relationship,
)

from security.models import (
    Vulnerability,
)

from ingestion.models import (
    IngestionRun,
)

from .planner import (
    asset_ip_field_name,
    build_ingestion_plan,
)


class InvalidIngestionPlan(
    ValueError
):
    def __init__(
        self,
        plan,
    ):
        self.plan = plan

        super().__init__(
            (
                "The ingestion plan "
                "contains validation errors."
            )
        )


def _zone_for_name(
    organization,
    name,
):
    if not name:
        return None


    return (
        NetworkZone.objects.get(
            organization=organization,

            name__iexact=name,
        )
    )


@transaction.atomic
def apply_ingestion_bundle(
    *,
    organization,
    source_format,
    bundle,
):
    plan = build_ingestion_plan(
        organization,
        bundle,
    )


    if not plan[
        "valid"
    ]:
        raise InvalidIngestionPlan(
            plan
        )


    for item in (
        bundle.network_zones
    ):
        existing = (
            NetworkZone.objects.filter(
                organization=organization,

                name__iexact=item.name,
            )
            .order_by("id")
            .first()
        )


        if existing is None:
            existing = NetworkZone(
                organization=organization,

                name=item.name,
            )


        existing.zone_type = (
            item.zone_type
        )


        existing.full_clean()

        existing.save()


    ip_field = (
        asset_ip_field_name()
    )


    for item in bundle.assets:
        existing = (
            Asset.objects.filter(
                organization=organization,

                name__iexact=item.name,
            )
            .order_by("id")
            .first()
        )


        if existing is None:
            existing = Asset(
                organization=organization,

                name=item.name,
            )


        existing.asset_type = (
            item.asset_type
        )

        existing.criticality = (
            item.criticality
        )

        existing.environment = (
            item.environment
        )

        existing.hostname = (
            item.hostname
        )

        existing.is_internet_exposed = (
            item.is_internet_exposed
        )

        existing.network_zone = (
            _zone_for_name(
                organization,

                item
                .network_zone_name,
            )
        )


        if ip_field:
            setattr(
                existing,
                ip_field,
                item.ip_address,
            )


        existing.full_clean()

        existing.save()


    for item in (
        bundle.relationships
    ):
        source = Asset.objects.get(
            organization=organization,

            name__iexact=(
                item.source_name
            ),
        )


        target = Asset.objects.get(
            organization=organization,

            name__iexact=(
                item.target_name
            ),
        )


        existing = (
            Relationship.objects.filter(
                source=source,

                target=target,

                relationship_type=(
                    item
                    .relationship_type
                ),

                protocol=(
                    item.protocol
                ),

                port=item.port,
            )
            .order_by("id")
            .first()
        )


        if existing is None:
            existing = Relationship(
                source=source,

                target=target,

                relationship_type=(
                    item
                    .relationship_type
                ),

                protocol=item.protocol,

                port=item.port,
            )


        existing.requires_authentication = (
            item
            .requires_authentication
        )

        existing.required_source_privilege = (
            item
            .required_source_privilege
        )


        existing.full_clean()

        existing.save()


    for item in (
        bundle.vulnerabilities
    ):
        asset = Asset.objects.get(
            organization=organization,

            name__iexact=(
                item.asset_name
            ),
        )


        if item.reference_id:
            existing = (
                Vulnerability.objects.filter(
                    asset=asset,

                    reference_id__iexact=(
                        item.reference_id
                    ),
                )
                .order_by("id")
                .first()
            )

        else:
            existing = (
                Vulnerability.objects.filter(
                    asset=asset,

                    title__iexact=(
                        item.title
                    ),
                )
                .order_by("id")
                .first()
            )


        if existing is None:
            existing = Vulnerability(
                asset=asset,
            )


        existing.reference_id = (
            item.reference_id
        )

        existing.title = (
            item.title
        )

        existing.cvss_score = (
            item.cvss_score
        )

        existing.attack_vector = (
            item.attack_vector
        )

        existing.privileges_required = (
            item.privileges_required
        )

        existing.grants_privilege = (
            item.grants_privilege
        )

        existing.bypasses_authentication = (
            item
            .bypasses_authentication
        )

        existing.bypasses_mfa = (
            item.bypasses_mfa
        )

        existing.is_exploitable = (
            item.is_exploitable
        )

        existing.description = (
            item.description
        )


        existing.full_clean()

        existing.save()


    run = IngestionRun.objects.create(
        organization=organization,

        source_format=source_format,

        source_files=list(
            bundle.source_files
        ),

        summary=plan[
            "summary"
        ],
    )


    return (
        run,
        plan,
    )
