from typing import ClassVar, Any

from config.settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


class MessageEmail:
    _EMAIL_HOST: ClassVar[str] = EMAIL_HOST_USER
    _template_html: ClassVar[str] = None
    _template_plaintext: ClassVar[str] = None
    _subject: ClassVar[Any] = None

    def _email_multi_alternatives(self, to: str, context: dict[str, Any]) -> EmailMultiAlternatives:
        return EmailMultiAlternatives(
            subject=self._subject,
            body=get_template(self._template_plaintext).render(context),
            from_email=self._EMAIL_HOST,
            to=[to]
        )

    def attach_alternative(self, to: str, context: dict[str, Any]):
        msg = self._email_multi_alternatives(to, context)
        msg.attach_alternative(get_template(self._template_html).render(context), "text/html")
        msg.send()


class MailUserCodeVerifications(MessageEmail):
    _template_html: ClassVar[str] = "messages_user.html"
    _template_plaintext: ClassVar[str] = "messages_user.txt"
    _subject: ClassVar[Any] = 'Codígo de verificación'

    def __init__(self, to: str, **kwargs):
        _context = {k: v for k, v in kwargs.items()}
        self.attach_alternative(to, _context)
