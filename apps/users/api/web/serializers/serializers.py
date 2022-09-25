from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework import serializers

from apps.users.exceptions import UserValidationException
from apps.users.models import User


class SerializerLoginUser(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        attr = dict(attrs)
        email = attr.get("email")
        password = attr.get("password")

        try:
            user: User = User.objects.get_user_instance(email)
        except (ObjectDoesNotExist, IntegrityError) as e:
            raise UserValidationException(2)

        if not user.check_password(password):
            raise UserValidationException(2)

        if not user.state:
            raise UserValidationException(3)

        return attrs

    def create(self, **kwargs) -> User:
        instance: User = User.objects.get_user_instance(self.validated_data.get("email"))
        instance.is_active = True
        instance.is_new = False
        instance.save()
        return instance
