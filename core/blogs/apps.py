from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BlogConfig(AppConfig):
    name = "core.blogs"
    verbose_name = _("Blogs")
