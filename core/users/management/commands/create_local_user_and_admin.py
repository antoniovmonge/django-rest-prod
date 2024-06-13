import sys

from allauth.account.models import EmailAddress
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

User = get_user_model()


class Command(BaseCommand):
    """
    Create the basic superuser
    """

    help = "Seed database with 'admin' and 'normal user'"

    def handle(self, *args, **options):
        if not settings.DEBUG:
            msg = (
                "This command cannot be run when settings DEBUG == False,"
                "to guard against accidental use on production."
            )
            raise CommandError(msg)
        # SuperUser
        if User.objects.filter(email="admin@email.com").exists():
            sys.stdout.write("The admin user already exists.")
        else:
            self.stdout.write("Creating local SUPER user...")
            create_local_superuser()
            self.stdout.write('Local superuser "admin" was created')
        # Local Normal User
        if User.objects.filter(email="user@email.com").exists():
            sys.stdout.write("The local default user already exists.")
        else:
            self.stdout.write("Creating local NORMAL user...")
            create_local_normal_user()
            self.stdout.write('Local local user "user" was created')


def create_local_superuser():
    User.objects.create_superuser(
        email="admin@email.com",
        password="testpass123",  # noqa: S106
        name="Admin",
    )
    EmailAddress.objects.create(
        user=User.objects.get(email="admin@email.com"),
        email="admin@email.com",
        verified=True,
        primary=True,
    )


def create_local_normal_user():
    User.objects.create_user(
        email="user@email.com",
        password="testpass123",  # noqa: S106
        name="user_00",
    )
    EmailAddress.objects.create(
        user=User.objects.get(email="user@email.com"),
        email="user@email.com",
        verified=True,
        primary=True,
    )
