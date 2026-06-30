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

    # Si el partido se definió en penales, aquí va el marcador de la tanda.
    penalties_team_1 = models.PositiveSmallIntegerField(
        "penales del equipo 1", null=True, blank=True
    )
    penalties_team_2 = models.PositiveSmallIntegerField(
        "penales del equipo 2", null=True, blank=True
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

    @property
    def went_to_penalties(self):
        return self.penalties_team_1 is not None and self.penalties_team_2 is not None

    @property
    def penalty_winner(self):
        """Ganador de la tanda de penales: 'team_1', 'team_2' o None."""
        if not self.went_to_penalties:
            return None
        if self.penalties_team_1 > self.penalties_team_2:
            return "team_1"
        if self.penalties_team_2 > self.penalties_team_1:
            return "team_2"
        return None

    @property
    def result_display(self):
        """Resultado legible, con la tanda de penales si la hubo."""
        if not self.has_result:
            return "—"
        marcador = f"{self.goals_team_1} : {self.goals_team_2}"
        if self.went_to_penalties:
            marcador += f" (pen. {self.penalties_team_1}-{self.penalties_team_2})"
        return marcador

    def __str__(self):
        return f"{self.team_1} vs {self.team_2} - {self.stage} ({self.date})"
