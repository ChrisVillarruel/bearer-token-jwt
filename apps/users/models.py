import datetime as dt
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

    def __str__(self) -> str:
        return self.hex_id

    @property
    def get_user_id(self):
        return self.id

    @staticmethod
    def _unix_time(date_time: dt.datetime):
        return dt.datetime.timestamp(date_time)

    def save(self, *args, **kwargs):
        self.hex_id = self.id_length.hex
        super().save(*args, **kwargs)
