import json

from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.urls import reverse


class ImportAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        self.url = "/api/v1/import/"

    def _perform_post(self, data):
        response = self.client.post(
            self.url, data=json.dumps(data), content_type="application/json"
        )
        return response.json(), response.status_code

    def test_import_valid_category(self):
        data = [
            {
                "categoryName": "T-shirts",
                "categoryCode": "t-shirts",
            }
        ]
        response, status_code = self._perform_post(data=data)
