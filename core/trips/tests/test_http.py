from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from core.trips.models import Trip

PASSWORD = "pAssw0rd!"  # noqa: S105


def create_user(email="testuser@email.com", password=PASSWORD):
    return get_user_model().objects.create_user(
        email=email,
        name="Test User",
        password=password,
    )


class HttpTripTest(APITestCase):
    def setUp(self):
        user = create_user()
        response = self.client.post(
            reverse("api-log-in"),
            data={
                "email": user.email,
                "password": PASSWORD,
            },
        )
        self.access = response.data["access"]

    def test_user_can_list_trips(self):
        trips = [
            Trip.objects.create(pick_up_address="A", drop_off_address="B"),
            Trip.objects.create(pick_up_address="B", drop_off_address="C"),
        ]
        response = self.client.get(
            reverse("trip:trip_list"),
            headers={"authorization": f"Bearer {self.access}"},
        )
        assert status.HTTP_200_OK, response.status_code
        exp_trip_ids = [str(trip.id) for trip in trips]
        act_trip_ids = [trip.get("id") for trip in response.data]
        assert exp_trip_ids, act_trip_ids

    def test_user_can_retrieve_trip_by_id(self):
        trip = Trip.objects.create(pick_up_address="A", drop_off_address="B")
        response = self.client.get(
            trip.get_absolute_url(),
            headers={"authorization": f"Bearer {self.access}"},
        )
        assert status.HTTP_200_OK, response.status_code
        assert str(trip.id), response.data.get("id")
