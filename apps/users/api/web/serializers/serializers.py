import datetime as dt
from typing import ClassVar

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.core.cache import cache

from rest_framework import serializers

from apps.users.exceptions import UserValidationException
from apps.users.models import User
from config.backends.authentication.cryptography_user_info import DecryptRSACryptography


class SerializerLoginUser(serializers.Serializer):
    _decrypt_password: ClassVar[DecryptRSACryptography] = DecryptRSACryptography
    email = serializers.CharField()
    password = serializers.CharField()

    @staticmethod
    def validate_email(value: str) -> str:
        return value.lower()

    def validate_password(self, value: str) -> None | str:
        try:
            return self._decrypt_password(value).decrypt_data
        except Exception as _:
            return None

    def validate(self, attrs):
        attr = dict(attrs)
        email = attr.get("email")
        password = attr.get("password")

        try:
            user: User = User.objects.get_user_instance(email)
        except (ObjectDoesNotExist, IntegrityError) as _:
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


class SerializerUpdateUserPassword(serializers.Serializer):
    _decrypt_password: ClassVar[DecryptRSACryptography] = DecryptRSACryptography
    password = serializers.CharField()
    new_password = serializers.CharField()

    def validate_password(self, value: str) -> str | None:
        try:
            return self._decrypt_password(value).decrypt_data
        except Exception as _:
            return None

    def validate_new_password(self, value: str) -> str | None:
        try:
            return self._decrypt_password(value).decrypt_data
        except Exception as _:
            return None

    def validate(self, attrs):
        attr = dict(attrs)
        password = attr.get("password")
        new_password = attr.get("new_password")
        user: User = self.context.get("user")

        if not user.check_password(password):
            raise UserValidationException(14)
        if not user.is_active:
            raise UserValidationException(15)
        if password == new_password:
            raise UserValidationException(16)
        if not user.state:
            raise UserValidationException(17)
        return attrs

    def update(self, **kwargs) -> User:
        instance: User = self.context.get("user")
        instance.set_password(self.validated_data.get("new_password"))
        instance.date_updated = dt.datetime.now()
        instance.is_active = False
        instance.save()
        return instance


class SerializersForgotPassword(serializers.Serializer):
    _decrypt_password: ClassVar[DecryptRSACryptography] = DecryptRSACryptography

    email = serializers.CharField()
    code = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate_new_password(self, value: str) -> None | str:
        try:
            return self._decrypt_password(value).decrypt_data
        except Exception as _:
            raise UserValidationException(500)

    def validate_confirm_password(self, value: str) -> None | str:
        try:
            return self._decrypt_password(value).decrypt_data
        except Exception as _:
            raise UserValidationException(500)

    def validate(self, attrs):
        attr = dict(attrs)
        email = attr.get("email")
        code = attr.get("code")
        new_password = attr.get("new_password")
        confirm_password = attr.get("confirm_password")

        try:
            user: User = User.objects.get_user_instance(email)
        except (ObjectDoesNotExist, IntegrityError) as _:
            raise UserValidationException(2)

        if cache.get(user.email, None) != code:
            raise UserValidationException(18)
        if user.check_password(new_password):
            raise UserValidationException(16)
        if not user.state:
            raise UserValidationException(15)
        if new_password != confirm_password:
            raise UserValidationException(19)
        return attrs

    def update_password(self, user: User):
        user.set_password(self.validated_data.get("new_password"))
        user.date_updated = dt.datetime.now()
        user.is_active = False
        user.save()
