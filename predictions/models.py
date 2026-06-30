from django.conf import settings
from django.db import models


class Prediction(models.Model):
    """Pronóstico de un usuario para un partido."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="predictions",
    )
    match = models.ForeignKey(
        "matches.Match",
        on_delete=models.CASCADE,
        related_name="predictions",
    )
    goals_team_1 = models.PositiveSmallIntegerField("goles equipo 1")
    goals_team_2 = models.PositiveSmallIntegerField("goles equipo 2")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "match")
        ordering = ["match__date"]

    def __str__(self):
        return f"{self.user} · {self.match}: {self.goals_team_1}-{self.goals_team_2}"

    @property
    def outcome(self):
        """Desenlace pronosticado: 'team_1', 'team_2' o 'draw'."""
        if self.goals_team_1 > self.goals_team_2:
            return "team_1"
        if self.goals_team_1 < self.goals_team_2:
            return "team_2"
        return "draw"

    @property
    def points(self):
        """Puntaje del pronóstico:

        - 3 puntos si acierta el resultado exacto del partido.
        - 1 punto si acierta el ganador (o empate) de los 90'.
        - Si el partido se definió en penales, también 1 punto si acertó al
          ganador de la tanda de penales.
        - 0 puntos en caso contrario.
        """
        match = self.match
        if not match.has_result:
            return 0
        if (
            self.goals_team_1 == match.goals_team_1
            and self.goals_team_2 == match.goals_team_2
        ):
            return 3
        if self.outcome == match.outcome:
            return 1
        if match.went_to_penalties and self.outcome == match.penalty_winner:
            return 1
        return 0
