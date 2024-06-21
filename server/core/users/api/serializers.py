from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from core.users.models import User


class UserSerializer(serializers.ModelSerializer[User]):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    group = serializers.CharField()

    def validate(self, data):
        if data["password1"] != data["password2"]:
            msg = "Passwords must match."
            raise serializers.ValidationError(msg)
        return data

    def create(self, validated_data):
        group_data = validated_data.pop("group")
        group, _ = Group.objects.get_or_create(name=group_data)
        data = {
            key: value
            for key, value in validated_data.items()
            if key not in ("password1", "password2")
        }
        data["password"] = validated_data["password1"]
        user = self.Meta.model.objects.create_user(**data)
        user.groups.add(group)
        user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = [
            "name",
            "url",
            "id",
            "password1",
            "password2",
            "email",
            "group",
            "photo",
        ]
        read_only_fields = ("id",)

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }


class LogInSerializer(TokenObtainPairSerializer):
    def get_token(self, user):
        token = super().get_token(user)
        user_data = UserSerializer(user, context=self.context).data
        for key, value in user_data.items():
            if key != "id":
                token[key] = value
        return token
