from rest_framework import (
    serializers,
)

from organizations.models import (
    Organization,
)

from .models import (
    IngestionRun,
)


MAX_FILE_SIZE = (
    5
    * 1024
    * 1024
)


class IngestionUploadSerializer(
    serializers.Serializer
):
    organization = (
        serializers
        .PrimaryKeyRelatedField(
            queryset=(
                Organization.objects.all()
            )
        )
    )


    source_format = (
        serializers.ChoiceField(
            choices=(
                "JSON",
                "CSV",
            )
        )
    )


    bundle_file = (
        serializers.FileField(
            required=False,
        )
    )


    network_zones_file = (
        serializers.FileField(
            required=False,
        )
    )


    assets_file = (
        serializers.FileField(
            required=False,
        )
    )


    relationships_file = (
        serializers.FileField(
            required=False,
        )
    )


    vulnerabilities_file = (
        serializers.FileField(
            required=False,
        )
    )


    def validate(self, attrs):
        source_format = attrs[
            "source_format"
        ]


        json_file = attrs.get(
            "bundle_file"
        )


        csv_fields = (
            "network_zones_file",
            "assets_file",
            "relationships_file",
            "vulnerabilities_file",
        )


        csv_files = [
            attrs.get(
                field_name
            )

            for field_name
            in csv_fields
        ]


        if (
            source_format
            == "JSON"
        ):
            if json_file is None:
                raise serializers.ValidationError(
                    {
                        "bundle_file": (
                            "A JSON bundle "
                            "file is required."
                        )
                    }
                )


            if any(
                csv_files
            ):
                raise serializers.ValidationError(
                    (
                        "CSV files must not "
                        "be supplied for a "
                        "JSON ingestion."
                    )
                )


        if (
            source_format
            == "CSV"
        ):
            if json_file is not None:
                raise serializers.ValidationError(
                    (
                        "bundle_file must not "
                        "be supplied for a "
                        "CSV ingestion."
                    )
                )


            if not any(
                csv_files
            ):
                raise serializers.ValidationError(
                    (
                        "Upload at least one "
                        "CSV file."
                    )
                )


        all_files = [
            json_file,
            *csv_files,
        ]


        for uploaded_file in all_files:
            if uploaded_file is None:
                continue


            if (
                uploaded_file.size
                > MAX_FILE_SIZE
            ):
                raise serializers.ValidationError(
                    (
                        f"{uploaded_file.name} "
                        "is larger than the "
                        "5 MB Phase 14 limit."
                    )
                )


        return attrs


class IngestionRunSerializer(
    serializers.ModelSerializer
):
    organization_name = (
        serializers.CharField(
            source="organization.name",

            read_only=True,
        )
    )


    source_format_display = (
        serializers.CharField(
            source=(
                "get_source_format_display"
            ),

            read_only=True,
        )
    )


    class Meta:
        model = IngestionRun

        fields = [
            "id",

            "organization",
            "organization_name",

            "source_format",
            "source_format_display",

            "source_files",

            "summary",

            "created_at",
        ]
