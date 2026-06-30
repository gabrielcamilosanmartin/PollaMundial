from django.contrib import admin

from .models import Match


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ("team_1", "team_2", "stage", "date", "goals_team_1", "goals_team_2")
    list_filter = ("stage",)
    search_fields = ("stage", "ground")
    ordering = ("date",)
