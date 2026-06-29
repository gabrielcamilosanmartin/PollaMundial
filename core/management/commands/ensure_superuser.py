"""Crea un superusuario a partir de variables de entorno, de forma idempotente.

Pensado para ejecutarse en cada despliegue (p. ej. en Render), donde no hay
acceso interactivo a `createsuperuser`. Lee:

    DJANGO_SUPERUSER_USERNAME  (obligatorio)
    DJANGO_SUPERUSER_PASSWORD  (obligatorio)
    DJANGO_SUPERUSER_EMAIL     (opcional)

Si faltan usuario o contraseña, no hace nada (no falla). Si el usuario ya
existe, tampoco hace nada. Así es seguro correrlo en cada build/deploy.
"""

import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Crea un superusuario desde variables de entorno si aún no existe."

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")

        if not username or not password:
            self.stdout.write(
                "DJANGO_SUPERUSER_USERNAME/PASSWORD no definidos; se omite la "
                "creación del superusuario."
            )
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                f"El superusuario '{username}' ya existe; no se crea de nuevo."
            )
            return

        User.objects.create_superuser(
            username=username, email=email, password=password
        )
        self.stdout.write(
            self.style.SUCCESS(f"Superusuario '{username}' creado correctamente.")
        )
