from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from common.mixins import StaffRequiredMixin

from .forms import MatchCreateForm, MatchUpdateForm
from .models import Match


class MatchListView(StaffRequiredMixin, ListView):
    model = Match
    template_name = "matches/match_list.html"
    context_object_name = "matches"
    ordering = ["date"]


class MatchCreateView(StaffRequiredMixin, CreateView):
    model = Match
    form_class = MatchCreateForm
    template_name = "matches/match_form.html"
    success_url = reverse_lazy("match_list")
    extra_context = {"title": "Crear partido"}


class MatchUpdateView(StaffRequiredMixin, UpdateView):
    model = Match
    form_class = MatchUpdateForm
    template_name = "matches/match_form.html"
    success_url = reverse_lazy("match_list")
    extra_context = {"title": "Editar partido"}


class MatchDeleteView(StaffRequiredMixin, DeleteView):
    model = Match
    template_name = "matches/match_confirm_delete.html"
    success_url = reverse_lazy("match_list")
