from django import forms

from common.forms import TailwindFormMixin

from .models import Match

MATCH_FIELDS = (
    "ground",
    "stage",
    "date",
    "team_1",
    "team_2",
    "is_draw",
    "winner",
    "result",
    "is_finished",
)


class MatchCreateForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Match
        fields = MATCH_FIELDS


class MatchUpdateForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Match
        fields = MATCH_FIELDS
