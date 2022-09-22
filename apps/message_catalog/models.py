from typing import Union

from django.db import models


class ManagerOperationCatalog(models.Manager):
    def create_operation_catalog(self, **kwargs):
        cat_error = self.model(
            name=kwargs.get("name"),
            description=kwargs.get("description"),
        )

        cat_error.save()
        return cat_error


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


class ManagerMessageCatalog(models.Manager):
    def create_message_catalog(self, **kwargs):
        cat_error = self.model(
            code_error=kwargs.get("code_error"),
            message=kwargs.get("message"),
            method_id=kwargs.get("method_id"),
        )

        cat_error.save()
        return cat_error

    def get_code_message(self, code: Union[str, int]):
        code_error = code
        if isinstance(code, str):
            code_error = int(code)

        return (
            super()
            .get_queryset()
            .filter(
                code_error=code_error
            )
            .values(
                "code_error",
                "message"
            )
            .first()
        )


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
