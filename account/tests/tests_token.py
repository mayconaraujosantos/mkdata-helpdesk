from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from account.models import User


class TokenTests(APITestCase):
    token_obtain_pair = reverse("token_obtain_pair")

    def setUp(self) -> None:
        self.user_data = {"username": "admin", "password": "admin"}
        self.user = User.objects.create_superuser(
            **self.user_data, is_staff=True, is_superuser=True, name="admin"
        )
        self.client.force_authenticate(user=self.user)

    def test_token_creation(self):
        url = self.token_obtain_pair
        response = self.client.post(url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_token_refresh(self):
        access_token = self.client.post(
            self.token_obtain_pair, self.user_data, format="json"
        ).data["refresh"]
        url = reverse("token_refresh")
        response = self.client.post(url, {"refresh": access_token}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_token_verification(self):
        access_token = self.client.post(
            self.token_obtain_pair, self.user_data, format="json"
        ).data["access"]
        url = reverse("token_verify")
        response = self.client.post(url, {"token": access_token}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
