from unittest.mock import patch

import pytest
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework_simplejwt.tokens import AccessToken

from config.asgi import application

TEST_CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}


@database_sync_to_async
def create_user(
    email,
    password,
    group="rider",
):
    # Create user.
    user = get_user_model().objects.create_user(
        email=email,
        password=password,
    )

    # Create user group.
    user_group, _ = Group.objects.get_or_create(name=group)
    user.groups.add(user_group)
    user.save()

    # Create access token.
    access = AccessToken.for_user(user)

    return user, access


@pytest.mark.asyncio()
@pytest.mark.django_db(transaction=True)
class TestWebSocket:
    async def test_can_connect_to_server(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        _, access = await create_user("test.user@email.com", "testpass123")
        communicator = WebsocketCommunicator(
            application=application,
            path=f"/taxi/?token={access}",
        )
        connected, _ = await communicator.connect()
        assert connected is True
        await communicator.disconnect()

    async def test_can_send_and_receive_messages(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        _, access = await create_user("test.user@email.com", "testpass123")
        communicator = WebsocketCommunicator(
            application=application,
            path=f"/taxi/?token={access}",
        )
        await communicator.connect()
        message = {
            "type": "echo.message",
            "data": "This is a test message.",
        }
        await communicator.send_json_to(message)
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()

    async def test_cannot_connect_to_socket(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        communicator = WebsocketCommunicator(application=application, path="/taxi/")
        connected, _ = await communicator.connect()
        assert connected is False
        await communicator.disconnect()

    async def test_join_driver_pool(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        _, access = await create_user("test.driver@email.com", "testpass123", "driver")
        communicator = WebsocketCommunicator(
            application=application,
            path=f"/taxi/?token={access}",
        )
        await communicator.connect()
        message = {
            "type": "echo.message",
            "data": "This is a test message.",
        }
        channel_layer = get_channel_layer()
        await channel_layer.group_send("drivers", message=message)
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()

    @patch("django.http.request.HttpRequest.get_host")
    async def test_request_trip(self, mock_get_host, settings):
        mock_get_host.return_value = "testserver"
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        user, access = await create_user("test.user@email.com", "testpass123", "rider")
        communicator = WebsocketCommunicator(
            application=application,
            path=f"/taxi/?token={access}",
        )
        await communicator.connect()
        await communicator.send_json_to(
            {
                "type": "create.trip",
                "data": {
                    "pick_up_address": "Calle Real 123",
                    "drop_off_address": "Avenida de la Luz 456",
                    "rider": user.id,
                },
            },
        )
        response = await communicator.receive_json_from()
        response_data = response.get("data")
        assert response_data["id"] is not None
        assert response_data["pick_up_address"] == "Calle Real 123"
        assert response_data["drop_off_address"] == "Avenida de la Luz 456"
        assert response_data["status"] == "REQUESTED"
        assert response_data["rider"]["email"] == user.email
        assert response_data["driver"] is None
        await communicator.disconnect()
