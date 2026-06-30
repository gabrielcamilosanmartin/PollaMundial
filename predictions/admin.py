from django.contrib import admin

from .models import Prediction


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ("user", "match", "goals_team_1", "goals_team_2", "updated_at")
    list_filter = ("user",)
    search_fields = ("user__email", "match__stage")
