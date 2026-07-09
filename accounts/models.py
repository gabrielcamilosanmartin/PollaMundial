from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Usuario que inicia sesión con el nombre de usuario (username)."""

    # Si es True, se obliga al usuario a definir su contraseña en el primer login.
    # Se activa al crear usuarios desde el panel de administración.
    must_change_password = models.BooleanField(
        "debe cambiar la contraseña", default=False
    )

    def __str__(self):
        return self.username
