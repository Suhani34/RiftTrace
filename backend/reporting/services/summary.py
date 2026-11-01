from assets.models import (
    Asset,
    NetworkZone,
    Relationship,
)

from scenarios.models import (
    SavedScenario,
    ScenarioRun,
)

from security.models import (
    Vulnerability,
)


def build_reporting_summary(
    organization,
):
    scenarios = (
        SavedScenario.objects
        .filter(
            organization=organization
        )
    )


    runs = (
        ScenarioRun.objects
        .filter(
            scenario__organization=(
                organization
            )
        )
    )


    return {
        "organization": {
            "id":
                organization.id,

            "name":
                organization.name,
        },

        "environment": {
            "network_zones":
                NetworkZone.objects
                .filter(
                    organization=(
                        organization
                    )
                )
                .count(),

            "assets":
                Asset.objects
                .filter(
                    organization=(
                        organization
                    )
                )
                .count(),

            "relationships":
                Relationship.objects
                .filter(
                    source__organization=(
                        organization
                    )
                )
                .count(),

            "vulnerabilities":
                Vulnerability.objects
                .filter(
                    asset__organization=(
                        organization
                    )
                )
                .count(),
        },

        "scenarios": {
            "total":
                scenarios.count(),

            "runs":
                runs.count(),

            "successful_runs":
                runs.filter(
                    status=(
                        ScenarioRun
                        .Status
                        .SUCCESS
                    )
                )
                .count(),

            "failed_runs":
                runs.filter(
                    status=(
                        ScenarioRun
                        .Status
                        .FAILED
                    )
                )
                .count(),
        },
    }
