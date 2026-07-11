from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from common.mixins import StaffRequiredMixin

from . import services
from .forms import MatchCreateForm, MatchUpdateForm
from .models import Match


class MatchListView(StaffRequiredMixin, ListView):
    model = Match
    template_name = "matches/match_list.html"
    context_object_name = "matches"
    ordering = ["date"]

    def get_queryset(self):
        # Evita N+1: trae los equipos en una sola consulta (importante con
        # bases de datos remotas como Neon).
        return super().get_queryset().select_related("team_1", "team_2")


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


class MatchSyncView(StaffRequiredMixin, View):
    """Sincroniza los partidos de la API openfootball con la BD local.

    GET  -> devuelve (JSON) los partidos NUEVOS que se agregarían.
    POST -> crea esos partidos nuevos y devuelve cuántos se crearon.
    """

    def get(self, request, *args, **kwargs):
        try:
            nuevos = services.get_new_matches()
        except Exception as exc:  # noqa: BLE001 - reportamos el error al usuario
            return JsonResponse(
                {"error": f"No se pudo consultar la API: {exc}"}, status=502
            )

        return JsonResponse(
            {
                "count": len(nuevos),
                "matches": [
                    {
                        "team_1": n["team_1"].name,
                        "team_2": n["team_2"].name,
                        "stage": n["stage"],
                        "date": n["date"].strftime("%d/%m/%Y %H:%M"),
                        "ground": n["ground"] or "",
                    }
                    for n in nuevos
                ],
            }
        )

    def post(self, request, *args, **kwargs):
        try:
            nuevos = services.get_new_matches()
            creados = services.create_matches(nuevos)
        except Exception as exc:  # noqa: BLE001
            return JsonResponse(
                {"error": f"No se pudo consultar la API: {exc}"}, status=502
            )

        return JsonResponse({"created": creados})
