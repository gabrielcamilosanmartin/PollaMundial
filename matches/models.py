from django.db import models
from django.utils import timezone


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

    @property
    def has_result(self):
        return self.goals_team_1 is not None and self.goals_team_2 is not None

    @property
    def outcome(self):
        """Desenlace del partido: 'team_1', 'team_2', 'draw' o None si no hay resultado."""
        if not self.has_result:
            return None
        if self.goals_team_1 > self.goals_team_2:
            return "team_1"
        if self.goals_team_1 < self.goals_team_2:
            return "team_2"
        return "draw"

    @property
    def has_started(self):
        return timezone.now() >= self.date

    def __str__(self):
        return f"{self.team_1} vs {self.team_2} - {self.stage} ({self.date})"
