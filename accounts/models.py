from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    """Usuario que inicia sesión con el email (sin nombre de usuario)."""

    username = None
    email = models.EmailField("correo electrónico", unique=True)

    # Si es True, se obliga al usuario a definir su contraseña en el primer login.
    # Se activa al crear usuarios desde el panel de administración.
    must_change_password = models.BooleanField(
        "debe cambiar la contraseña", default=False
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
