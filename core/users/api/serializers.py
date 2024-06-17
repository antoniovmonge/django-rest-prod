from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.users.models import User


class UserSerializer(serializers.ModelSerializer[User]):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["password1"] != data["password2"]:
            msg = "Passwords must match."
            raise serializers.ValidationError(msg)
        return data

    def create(self, validated_data):
        data = {
            key: value
            for key, value in validated_data.items()
            if key not in ("password1", "password2")
        }
        data["password"] = validated_data["password1"]
        return self.Meta.model.objects.create_user(**data)

    class Meta:
        model = get_user_model()
        fields = [
            "name",
            "url",
            "id",
            "password1",
            "password2",
            "email",
        ]
        read_only_fields = ("id",)

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }
