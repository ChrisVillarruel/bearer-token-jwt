import datetime as dt
import random
import string
import uuid

from apps.base.models import BaseModel

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from apps.users.manager import UserManager


class User(AbstractBaseUser, BaseModel):
    id = models.AutoField(primary_key=True, editable=False, unique=True)
    id_length = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    hex_id = models.CharField(null=True, max_length=32, blank=True)
    email = models.CharField(max_length=255, unique=True, null=False)
    username = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=True)
    mother_last_name = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Users"
        verbose_name_plural = "User"
        db_table = "User"

    def __str__(self):
        return self.hex_id

    @staticmethod
    def _spilt_string(data: str) -> list[str]:
        if data:
            return data.upper().split()
        return "".split()

    @property
    def _random_string(self) -> str:
        return "".join(random.choices(string.ascii_uppercase, k=12))

    @property
    def generate_username(self) -> str:
        name: list[str] = self._spilt_string(str(self.name))
        last_name: list[str] = self._spilt_string(str(self.last_name))
        mother_last_name: list[str] = self._spilt_string(str(self.mother_last_name))
        ascii_uppercase = self._random_string.split()

        name.extend(last_name)
        name.extend(mother_last_name)
        name.extend(ascii_uppercase)
        return "".join(name)

    @property
    def get_user_id(self):
        return self.id

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
