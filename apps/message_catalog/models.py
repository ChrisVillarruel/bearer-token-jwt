from django.db import models

from apps.message_catalog.manager import ManagerOperationCatalog, ManagerMessageCatalog


class OperationCatalog(models.Model):
    """ Catalogo de tipo de operación logica """

    id = models.AutoField(primary_key=True, editable=False, unique=True)
    name = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=255, null=False)
    objects = ManagerOperationCatalog()

    class Meta:
        verbose_name = "OperationCatalog"
        verbose_name_plural = "OperationCatalog"
        db_table = "OperationCatalog"


class MessageCatalog(models.Model):
    id = models.AutoField(primary_key=True, editable=False, unique=True)
    code_error = models.IntegerField(null=False)
    message = models.CharField(max_length=255, null=False)
    method = models.ForeignKey(OperationCatalog, on_delete=models.DO_NOTHING, null=False)
    objects = ManagerMessageCatalog()

    class Meta:
        verbose_name = "MessageCatalog"
        verbose_name_plural = "MessageCatalog"
        db_table = "MessageCatalog"
