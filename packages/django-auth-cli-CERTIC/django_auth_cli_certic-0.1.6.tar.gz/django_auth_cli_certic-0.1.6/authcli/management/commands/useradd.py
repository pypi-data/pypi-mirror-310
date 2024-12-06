from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.contrib.auth import get_user_model

User = get_user_model()
import string
import secrets


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser):
        parser.add_argument(
            "-i", "--interactive", action="store_true", help="mode interactif"
        )
        parser.add_argument(
            "-a", "--active", action="store_true", help="utilisateur actif"
        )
        parser.add_argument(
            "-r",
            "--root",
            action="store_true",
            help="utilisateur est admin (superuser)",
        )
        parser.add_argument(
            "-s", "--staff", action="store_true", help="utilisateur est is_staff"
        )
        parser.add_argument(
            "-l", "--login", default=None, help="login (username) de l'utilisateur"
        )
        parser.add_argument(
            "-p", "--password", default=None, help="mot de passe de l'utilisateur"
        )
        parser.add_argument(
            "-e", "--email", default=None, help="email de l'utilisateur"
        )

    def handle(self, *args, **options):
        interactive = options["interactive"]
        user_login = options["login"]
        user_email = options["email"]
        user_password = options["password"]
        user_is_active = options["active"]
        user_is_staff = options["staff"]
        user_is_root = options["root"]

        if interactive:
            while not user_login:
                user_login = input("Login du nouvel utilisateur: ").strip()
            user_email = input(f"Email: ") or None
            user_password = input(f"Mot de passe: ") or None
            set_active = input("Actif ? (y/N): ")
            if set_active == "y":
                user_is_active = True
            set_is_staff = input("Statut équipe ? (y/N): ")
            if set_is_staff == "y":
                user_is_staff = True
            set_is_root = input("Statut superuser ? (y/N): ")
            if set_is_root == "y":
                user_is_root = True

        if not user_password:
            user_password = "".join(
                secrets.choice(
                    string.ascii_letters + string.digits + string.punctuation
                )
                for i in range(32)
            )

        if not user_login:
            raise CommandError("Le login de l'utilisateur est manquant")

        existing_user = User.objects.filter(username=user_login).first()
        if existing_user:
            raise CommandError("L'utilisateur existe déjà")

        user = User.objects.create_user(
            user_login,
            user_email,
            user_password,
            is_active=user_is_active,
            is_staff=user_is_staff,
            is_superuser=user_is_root,
        )
