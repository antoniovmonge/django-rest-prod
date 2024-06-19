import base64
import json
from io import BytesIO

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate

PASSWORD = "testpass123!"  # noqa: S105


def create_user(email="testuser@email.com", password=PASSWORD, group_name="rider"):
    group, _ = Group.objects.get_or_create(name=group_name)
    user = get_user_model().objects.create_user(email=email, password=password)
    user.groups.add(group)
    user.save()
    return user


def create_photo_file():
    data = BytesIO()
    Image.new("RGB", (100, 100)).save(data, "PNG")
    data.seek(0)
    return SimpleUploadedFile("photo.png", data.getvalue())


class AuthenticationTest(APITestCase):
    def test_user_can_signup(self):
        photo_file = create_photo_file()
        response = self.client.post(
            reverse("api-signup"),
            data={
                "email": "testuser@email.com",
                "name": "Test User",
                "password1": PASSWORD,
                "password2": PASSWORD,
                "group": "rider",
                "photo": photo_file,
            },
            follow=True,
        )
        user = get_user_model().objects.last()
        assert status.HTTP_201_CREATED, response.status_code
        assert response.data["id"] == user.id
        assert response.data["email"], user.email
        assert response.data["name"], user.name
        assert response.data["group"], user.group
        assert user.photo is not None

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
