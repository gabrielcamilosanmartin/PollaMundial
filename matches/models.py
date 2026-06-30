from django.core.exceptions import ValidationError
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

    is_draw = models.BooleanField("empate", default=False)
    winner = models.ForeignKey(
        "countries.Country",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="winner",
    )
    result = models.CharField(
        "resultado del partido", max_length=10, null=True, blank=True
    )

    is_finished = models.BooleanField("partido finalizado", default=False)

    class Meta:
        verbose_name = "partido"
        verbose_name_plural = "partidos"
        ordering = ["date"]

    def clean(self):
        super().clean()

        if self.winner_id is None:
            return

        allowed_winners = {self.team_1_id, self.team_2_id}
        if self.winner_id not in allowed_winners:
            raise ValidationError(
                {
                    "winner": "El ganador debe ser el equipo 1, el equipo 2 o quedar en empate (sin ganador).",
                }
            )

    def __str__(self):
        return f"{self.team_1} vs {self.team_2} - {self.stage} ({self.date})"
