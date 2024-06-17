from rest_framework import permissions
from rest_framework import viewsets

from core.trips.api.serializers import TripSerializer
from core.trips.models import Trip


class TripView(viewsets.ReadOnlyModelViewSet):
    lookup_field = "id"
    lookup_url_kwarg = "trip_id"
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
