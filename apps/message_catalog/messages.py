from typing import Dict, Any
from .models import MessageCatalog


class MyValidationError:
    def __init__(self, cat_error_id: str | int, status_code: int = 400):
        self.cat_error_id = cat_error_id
        self.status_code = status_code
        self.errors = self._get_error_code

    @property
    def _get_error_code(self) -> Dict[str, Any]:
        return MessageCatalog.objects.get_code_error(self.cat_error_id)

    @property
    def validation_error(self) -> Dict[str, Any]:
        return {
            "StatusCode": self.status_code,
            "ErrorCode": str(self._get_error_code.get("code_error")),
            "ErrorMessage": self._get_error_code.get("message")
        }


class MySuccessResponse:
    def __init__(self, cat_success_id: int, status_code: int = 200, **kwargs):
        self.success = cat_success_id
        self.status_code = status_code
        self.data = kwargs.get("data", None)

    @property
    def success_response(self) -> Dict[str, Any]:
        return {
            "StatusCode": self.status_code,
            "ErrorCode": self.success,
            "ExtraData": self.data
        }


class MyErrorResponse:
    def __init__(self, cat_error_id: int, status_code: int = 400):
        self.cat_error_id = cat_error_id
        self.status_code = status_code

    @property
    def error_response(self) -> Dict[str, Any]:
        return {
            "StatusCode": self.status_code,
            "ErrorCode": self.cat_error_id,
        }
