from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

PASSWORD = "pAssw0rd!"  # noqa: S105


class AuthenticationTest(APITestCase):
    def test_user_can_signup(self):
        response = self.client.post(
            reverse("signup"),
            data={
                "email": "user@example.com",
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
