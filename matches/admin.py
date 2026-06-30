from django.contrib import admin

from .models import Match


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ("team_1", "team_2", "stage", "date", "is_finished")
    list_filter = ("stage", "is_finished", "is_draw")
    search_fields = ("stage", "ground")
    ordering = ("date",)
