from rest_framework import serializers

from core.blogs import models


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Blog
        fields = "__all__"
        read_only_fields = ["updated_at"]
