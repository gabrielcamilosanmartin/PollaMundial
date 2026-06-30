from django import forms

from common.forms import TailwindFormMixin

from .models import Match

MATCH_FIELDS = (
    "ground",
    "stage",
    "date",
    "team_1",
    "team_2",
    "goals_team_1",
    "goals_team_2",
)


class MatchCreateForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Match
        fields = MATCH_FIELDS


class MatchUpdateForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Match
        fields = MATCH_FIELDS
