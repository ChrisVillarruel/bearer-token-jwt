from typing import Any

from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, **kwargs) -> object:
        user = self.model(
            email=self.normalize_email(kwargs.get("email")),
            password=kwargs.get("password"),
            name=kwargs.get("name"),
            last_name=kwargs.get("last_name"),
            mother_last_name=kwargs.get("mother_last_name"),
        )

        user.username = user.generate_username
        user.hex_id = user.id_length.hex
        user.set_password(user.password)
        user.save()
        return user

    def get_user_instance(self, email: str):
        return (
            super()
            .get_queryset()
            .get(
                email=email,
            )
        )

    def get_info_user(self, user_id: int) -> dict[str, Any]:
        return (
            super()
            .get_queryset()
            .filter(
                id=user_id
            )
            .values(
                "id",
                "email",
                "username",
                "name",
                "last_name",
                "mother_last_name",
                "is_active",
                "is_new",
                "last_login",
                "state",
            )
            .first()
        )
