from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

# Create your tests here.


def test_jwt_token_retrieve():
    client = APIClient()
    url = reverse("token_obtain_pair")
    data = {"username": "testuser", "password": "testpassword"}
    response = client.post(url, data, format="json")
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data
