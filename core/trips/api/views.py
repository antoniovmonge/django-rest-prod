from django.db.models import Q
from rest_framework import permissions
from rest_framework import viewsets

from core.trips.api.serializers import NestedTripSerializer
from core.trips.models import Trip


class TripView(viewsets.ReadOnlyModelViewSet):
    lookup_field = "id"
    lookup_url_kwarg = "trip_id"
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = NestedTripSerializer

    def get_queryset(self):
        user = self.request.user
        if user.group == "driver":
            return Trip.objects.filter(
                Q(status=Trip.REQUESTED) | Q(driver=user),
            )
        if user.group == "rider":
            return Trip.objects.filter(rider=user)
        return Trip.objects.none()
