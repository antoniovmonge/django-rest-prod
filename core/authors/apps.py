from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AuthorConfig(AppConfig):
    name = "core.authors"
    verbose_name = _("Authors")
