from rest_framework import viewsets

from core.authors.api.serializers import AuthorSerializer
from core.authors.models import Author


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
