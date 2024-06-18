import base64
import json

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate

PASSWORD = "testpass123!"  # noqa: S105


def create_user(email="testuser@email.com", password=PASSWORD):
    return get_user_model().objects.create_user(
        email=email,
        name="Test User",
        password=password,
    )


class AuthenticationTest(APITestCase):
    def test_user_can_signup(self):
        response = self.client.post(
            reverse("api-signup"),
            data={
                "email": "testuser@email.com",
                "name": "Test User",
                "password1": PASSWORD,
                "password2": PASSWORD,
            },
            follow=True,
        )
        user = get_user_model().objects.last()
        assert status.HTTP_201_CREATED, response.status_code
        assert response.data["id"] == user.id
        assert response.data["email"], user.email
        assert response.data["name"], user.name

    def test_user_can_log_in(self):
        user = create_user()
        factory = APIRequestFactory()
        request = factory.post(
            reverse("api-log-in"),
            data={
                "email": user.email,
                "password": PASSWORD,
            },
        )
        force_authenticate(request, user=user)

        response = self.client.post(
            reverse("api-log-in"),
            data={
                "email": user.email,
                "password": PASSWORD,
            },
        )

        access = response.data["access"]
        header, payload, signature = access.split(".")
        decoded_payload = base64.b64decode(f"{payload}==")
        payload_data = json.loads(decoded_payload)

        assert status.HTTP_200_OK, response.status_code
        assert response.data["refresh"]
        assert payload_data["id"], user.id
        assert payload_data["email"], user.email
        assert payload_data["name"], user.name
