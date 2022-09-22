from django.db import models


class ManagerOperationCatalog(models.Manager):
    def create_operation_catalog(self, **kwargs):
        cat_error = self.model(
            name=kwargs.get("name"),
            description=kwargs.get("description"),
        )

        cat_error.save()
        return cat_error


class ManagerMessageCatalog(models.Manager):
    def create_message_catalog(self, **kwargs):
        cat_error = self.model(
            code_error=kwargs.get("code_error"),
            message=kwargs.get("message"),
            method_id=kwargs.get("method_id"),
        )

        cat_error.save()
        return cat_error

    def get_code_message(self, code: str | int):
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
