"""Crea un superusuario a partir de variables de entorno, de forma idempotente.

Pensado para ejecutarse en cada despliegue (p. ej. en Render), donde no hay
acceso interactivo a `createsuperuser`. Lee:

    DJANGO_SUPERUSER_EMAIL     (obligatorio, es el identificador de login)
    DJANGO_SUPERUSER_PASSWORD  (obligatorio)

Si faltan email o contraseña, no hace nada (no falla). Si el usuario ya
existe, tampoco hace nada. Así es seguro correrlo en cada build/deploy.
"""

import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Crea un superusuario desde variables de entorno si aún no existe."

    def handle(self, *args, **options):
        User = get_user_model()

        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not email or not password:
            self.stdout.write(
                "DJANGO_SUPERUSER_EMAIL/PASSWORD no definidos; se omite la "
                "creación del superusuario."
            )
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(
                f"El superusuario '{email}' ya existe; no se crea de nuevo."
            )
            return

        User.objects.create_superuser(email=email, password=password)
        self.stdout.write(
            self.style.SUCCESS(f"Superusuario '{email}' creado correctamente.")
        )
