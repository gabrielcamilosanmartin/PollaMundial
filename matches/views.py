import json
import urllib.request
from datetime import datetime, timedelta, timezone

from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from common.mixins import StaffRequiredMixin
from countries.models import Country

from .forms import MatchCreateForm, MatchUpdateForm
from .models import Match

API_URL = (
    "https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json"
)


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


def _parse_datetime(date_str, time_str):
    """Combina la fecha y la hora de la API en un datetime con zona horaria.

    `time_str` viene como "13:00 UTC-6" (hora + desfase respecto a UTC).
    """
    hhmm, _, tz_part = (time_str or "").partition(" ")
    offset_minutes = 0
    tz_part = tz_part.strip().upper()
    if tz_part.startswith("UTC"):
        raw = tz_part[3:]  # p. ej. "-6" o "-6:30"
        if raw:
            negative = raw.startswith("-")
            raw = raw.lstrip("+-")
            if ":" in raw:
                hours, minutes = raw.split(":")
                offset_minutes = int(hours) * 60 + int(minutes)
            else:
                offset_minutes = int(raw) * 60
            if negative:
                offset_minutes = -offset_minutes

    tzinfo = timezone(timedelta(minutes=offset_minutes))
    try:
        naive = datetime.strptime(f"{date_str} {hhmm}", "%Y-%m-%d %H:%M")
    except ValueError:
        naive = datetime.strptime(date_str, "%Y-%m-%d")
    return naive.replace(tzinfo=tzinfo)


class MatchSyncView(StaffRequiredMixin, View):
    """Sincroniza los partidos de la API openfootball con la BD local.

    GET  -> calcula y devuelve (JSON) los partidos NUEVOS que se agregarían.
    POST -> crea esos partidos nuevos y devuelve cuántos se crearon.
    """

    def _fetch_matches(self):
        request = urllib.request.Request(
            API_URL, headers={"User-Agent": "PollaMundial"}
        )
        with urllib.request.urlopen(request, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
        return data.get("matches", [])

    def _new_matches(self):
        """Lista de partidos de la API que aún no están en la BD.

        Se omiten los que tengan algún equipo cuyo `code` no exista en Country.
        """
        countries = {c.code: c for c in Country.objects.all()}
        nuevos = []
        for item in self._fetch_matches():
            team_1 = countries.get(item.get("team1"))
            team_2 = countries.get(item.get("team2"))
            if team_1 is None or team_2 is None:
                continue

            stage = item.get("group") or item.get("round") or ""
            fecha = _parse_datetime(item.get("date"), item.get("time"))
            ground = item.get("ground") or None

            ya_existe = Match.objects.filter(
                team_1=team_1, team_2=team_2, date=fecha
            ).exists()
            if ya_existe:
                continue

            nuevos.append(
                {
                    "team_1": team_1,
                    "team_2": team_2,
                    "stage": stage,
                    "date": fecha,
                    "ground": ground,
                }
            )
        return nuevos

    def get(self, request, *args, **kwargs):
        try:
            nuevos = self._new_matches()
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
            nuevos = self._new_matches()
        except Exception as exc:  # noqa: BLE001
            return JsonResponse(
                {"error": f"No se pudo consultar la API: {exc}"}, status=502
            )

        creados = 0
        for n in nuevos:
            Match.objects.create(
                team_1=n["team_1"],
                team_2=n["team_2"],
                stage=n["stage"],
                date=n["date"],
                ground=n["ground"],
            )
            creados += 1

        return JsonResponse({"created": creados})
