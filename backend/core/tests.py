from django.test import SimpleTestCase
from django.urls import reverse

class HealthEndpointTests(SimpleTestCase):
	def test_health_endpoint_return_ok(self):
		response = self.client.get(reverse("core:health"))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json()["status"], "ok")
		self.assertEqual(response.json()["service"], "rifttrace-backend")
