from django.db import models


class BaseModel(models.Model):
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    state = models.BooleanField(default=True)

    class Meta:
        abstract = True
