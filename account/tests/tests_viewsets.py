from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from account.constants import CHANGE_PASSWORD_URL
from account.models import User
from account.viewsets import UserViewSet


class UserViewSetTestCase(APITestCase):
    def setUp(self):
        self.viewset = UserViewSet()
        self.user = User.objects.create_superuser(
            username="jorge",
            name="marcos",
            password="admin",
            is_staff=True,
            is_superuser=True,
        )
        self.client.force_authenticate(user=self.user)

    def test_change_password_with_valid_data(self):
        response = self.perform_password_change_request()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"detail": True})

    def perform_password_change_request(self):
        url = reverse("user-detail", args=[self.user.pk])
        change_password_url = url + "change_password/"
        data = {
            "reset": False,
            "password": "admin",
            "new_password": "newpassword",
        }

        response = self.client.patch(change_password_url, data, format="json")
        return response

    def test_change_password_with_invalid_password(self):
        url = reverse("user-detail", args=[self.user.pk])
        change_password_url = url + CHANGE_PASSWORD_URL
        data = {
            "reset": False,
            "password": "wrongpassword",
            "new_password": "newpassword",
        }

        response = self.client.patch(change_password_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(
            response.data,
            {"detail": "Invalid password"},
        )

    def test_change_password_reset_password(self):
        url = reverse("user-detail", args=[self.user.pk])
        change_password_url = url + "change_password/"
        data = {
            "reset": True,
            "new_password": "newpassword",
        }

        response = self.client.patch(change_password_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"detail": True})
