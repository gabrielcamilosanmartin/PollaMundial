from django.db import models


class Match(models.Model):
    """Registro del partido de futbol."""

    ground = models.CharField("estadio", max_length=100, null=True, blank=True)
    stage = models.CharField("etapa del torneo", max_length=100)
    date = models.DateTimeField("fecha del partido")
    team_1 = models.ForeignKey(
        "countries.Country", on_delete=models.CASCADE, related_name="team_1"
    )
    team_2 = models.ForeignKey(
        "countries.Country", on_delete=models.CASCADE, related_name="team_2"
    )

    goals_team_1 = models.PositiveSmallIntegerField(
        "goles del equipo 1", null=True, blank=True
    )
    goals_team_2 = models.PositiveSmallIntegerField(
        "goles del equipo 2", null=True, blank=True
    )

    class Meta:
        verbose_name = "partido"
        verbose_name_plural = "partidos"
        ordering = ["date"]

    def __str__(self):
        return f"{self.team_1} vs {self.team_2} - {self.stage} ({self.date})"
