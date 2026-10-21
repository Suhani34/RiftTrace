from django.core.management import (
    call_command,
)

from django.urls import reverse

from rest_framework import status

from rest_framework.test import (
    APITestCase,
)


class AttackMappingAPITests(
    APITestCase
):
    @classmethod
    def setUpTestData(cls):
        call_command(
            "seed_attack_catalog"
        )


    def test_attack_catalog_contains_expected_techniques(
        self,
    ):
        response = self.client.get(
            "/api/attack/techniques/"
        )


        self.assertEqual(
            response.status_code,

            status.HTTP_200_OK,
        )


        ids = {
            item[
                "attack_id"
            ]

            for item
            in response.data
        }


        self.assertEqual(
            ids,

            {
                "T1190",
                "T1552",
                "T1078",
                "T1021",
            },
        )


    def test_remote_service_event_maps_to_valid_accounts_and_remote_services(
        self,
    ):
        response = self.client.post(
            reverse(
                "attack-mapping-evaluate"
            ),

            {
                "event_type":
                    "IDENTITY_ACCESS",

                "attributes": {
                    "access_type":
                        "REMOTE_SERVICE"
                },
            },

            format="json",
        )


        self.assertEqual(
            response.status_code,

            status.HTTP_200_OK,
        )


        ids = {
            item[
                "attack_id"
            ]

            for item
            in response.data[
                "annotations"
            ]
        }


        self.assertEqual(
            ids,

            {
                "T1078",
                "T1021",
            },
        )


    def test_internal_vulnerability_does_not_map_to_t1190(
        self,
    ):
        response = self.client.post(
            reverse(
                "attack-mapping-evaluate"
            ),

            {
                "event_type":
                    (
                        "VULNERABILITY_EXPLOIT"
                    ),

                "attributes": {
                    "internet_exposed":
                        False
                },
            },

            format="json",
        )


        ids = {
            item[
                "attack_id"
            ]

            for item
            in response.data[
                "annotations"
            ]
        }


        self.assertNotIn(
            "T1190",
            ids,
        )
