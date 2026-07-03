from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, TemplateView

from common.mixins import StaffRequiredMixin
from matches.models import Match
from matches.services import update_results_from_api

from .models import Prediction

User = get_user_model()


def _participant_name(user):
    return user.first_name or user.email


class HomeView(LoginRequiredMixin, View):
    """Página principal: lista de partidos y envío de pronósticos."""

    template_name = "predictions/home.html"

    def _matches_with_predictions(self, user):
        # Partidos de hoy en adelante (no se muestran los de días anteriores).
        # Los que ya comenzaron se muestran pero con los inputs deshabilitados.
        start_of_today = timezone.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        matches = list(
            Match.objects.filter(date__gte=start_of_today)
            .select_related("team_1", "team_2")
            .order_by("date")
        )
        mis_pred = {
            p.match_id: p
            for p in Prediction.objects.filter(user=user, match__in=matches)
        }
        for match in matches:
            match.my_prediction = mis_pred.get(match.id)
        return matches

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
            {
                "matches": self._matches_with_predictions(request.user),
                "saved": request.GET.get("ok") == "1",
            },
        )

    def post(self, request, *args, **kwargs):
        for match in Match.objects.all():
            if match.has_started:
                continue  # no se aceptan pronósticos de partidos ya comenzados
            g1 = request.POST.get(f"goals_team_1_{match.id}", "").strip()
            g2 = request.POST.get(f"goals_team_2_{match.id}", "").strip()
            if g1 == "" or g2 == "":
                continue
            try:
                g1, g2 = int(g1), int(g2)
            except ValueError:
                continue
            if g1 < 0 or g2 < 0:
                continue
            Prediction.objects.update_or_create(
                user=request.user,
                match=match,
                defaults={"goals_team_1": g1, "goals_team_2": g2},
            )
        return redirect(reverse("home") + "?ok=1")


class MyPredictionsView(LoginRequiredMixin, TemplateView):
    """Pronósticos de todos los participantes para los partidos finalizados."""

    template_name = "predictions/my_predictions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Partidos que ya comenzaron (con o sin resultado todavía).
        matches = list(
            Match.objects.filter(date__lte=timezone.now())
            .select_related("team_1", "team_2")
            .order_by("-date")
        )
        users = list(User.objects.order_by("first_name", "email"))
        preds = {
            (p.match_id, p.user_id): p
            for p in Prediction.objects.filter(match__in=matches)
        }

        rows = []
        for match in matches:
            cells = [preds.get((match.id, u.id)) for u in users]
            rows.append({"match": match, "cells": cells})

        context["participants"] = [
            {"user": u, "name": _participant_name(u)} for u in users
        ]
        context["rows"] = rows
        return context


class ResultsView(LoginRequiredMixin, TemplateView):
    """Resultados de los partidos y puntos por participante."""

    template_name = "predictions/results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Al abrir la página se actualizan los resultados desde la API.
        try:
            context["api_updated"] = update_results_from_api()
            context["api_error"] = None
        except Exception as exc:  # noqa: BLE001
            context["api_updated"] = 0
            context["api_error"] = str(exc)

        # Partidos que ya comenzaron (con o sin resultado todavía).
        matches = list(
            Match.objects.filter(date__lte=timezone.now())
            .select_related("team_1", "team_2")
            .order_by("-date")
        )
        users = list(User.objects.order_by("first_name", "email"))
        preds = {
            (p.match_id, p.user_id): p
            for p in Prediction.objects.filter(match__in=matches)
        }

        totals = {u.id: 0 for u in users}
        rows = []
        for match in matches:
            cells = []
            for user in users:
                prediction = preds.get((match.id, user.id))
                points = prediction.points if prediction else 0
                totals[user.id] += points
                cells.append({"prediction": prediction, "points": points})
            rows.append({"match": match, "cells": cells})

        leaderboard = sorted(users, key=lambda u: totals[u.id], reverse=True)

        context["participants"] = [
            {"user": u, "name": _participant_name(u)} for u in users
        ]
        context["rows"] = rows
        context["leaderboard"] = [
            {"name": _participant_name(u), "total": totals[u.id]} for u in leaderboard
        ]
        return context


# --- Administración de predicciones (solo staff) ---


class PredictionAdminListView(StaffRequiredMixin, ListView):
    """Lista de partidos para gestionar las predicciones de cada uno."""

    model = Match
    template_name = "predictions/admin_list.html"
    context_object_name = "matches"

    def get_queryset(self):
        return (
            Match.objects.select_related("team_1", "team_2")
            .annotate(num_preds=Count("predictions"))
            .order_by("date")
        )


class PredictionMatchEditView(StaffRequiredMixin, View):
    """Edita/añade las predicciones de TODOS los participantes para un partido.

    Pensado para cargar manualmente (backfill) las predicciones que llegaron por
    WhatsApp antes de existir la app, incluso para partidos ya cerrados.
    """

    template_name = "predictions/admin_match.html"

    def get(self, request, pk, *args, **kwargs):
        match = get_object_or_404(
            Match.objects.select_related("team_1", "team_2"), pk=pk
        )
        preds = {p.user_id: p for p in Prediction.objects.filter(match=match)}
        rows = [
            {
                "user": u,
                "name": _participant_name(u),
                "prediction": preds.get(u.id),
            }
            for u in User.objects.order_by("first_name", "email")
        ]
        return render(request, self.template_name, {"match": match, "rows": rows})

    def post(self, request, pk, *args, **kwargs):
        match = get_object_or_404(Match, pk=pk)
        for user in User.objects.all():
            g1 = request.POST.get(f"goals_team_1_{user.id}", "").strip()
            g2 = request.POST.get(f"goals_team_2_{user.id}", "").strip()

            if g1 == "" and g2 == "":
                # Ambos vacíos: si existía una predicción, se elimina.
                Prediction.objects.filter(user=user, match=match).delete()
                continue
            if g1 == "" or g2 == "":
                continue  # incompleto, se ignora
            try:
                g1, g2 = int(g1), int(g2)
            except ValueError:
                continue
            if g1 < 0 or g2 < 0:
                continue

            Prediction.objects.update_or_create(
                user=user,
                match=match,
                defaults={"goals_team_1": g1, "goals_team_2": g2},
            )
        return redirect(reverse("prediction_admin_list") + "?ok=1")
