from django.db import models


class Country(models.Model):
    """Registro de un país."""

    name = models.CharField("nombre del país", max_length=100, unique=True)
    code = models.CharField("código del país", max_length=100, unique=True)

    class Meta:
        verbose_name = "país"
        verbose_name_plural = "países"
        ordering = ["name"]

    def __str__(self):
        return self.name
