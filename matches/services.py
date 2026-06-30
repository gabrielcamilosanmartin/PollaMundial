"""Servicios para sincronizar partidos y resultados desde la API openfootball."""

import json
import urllib.request
from datetime import datetime, timedelta, timezone

from countries.models import Country

from .models import Match

API_URL = (
    "https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json"
)


def parse_datetime(date_str, time_str):
    """Combina fecha y hora de la API en un datetime con zona horaria.

    `time_str` viene como "13:00 UTC-6" (hora + desfase respecto a UTC).
    """
    hhmm, _, tz_part = (time_str or "").partition(" ")
    offset_minutes = 0
    tz_part = tz_part.strip().upper()
    if tz_part.startswith("UTC"):
        raw = tz_part[3:]
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


def fetch_api_matches():
    request = urllib.request.Request(API_URL, headers={"User-Agent": "PollaMundial"})
    with urllib.request.urlopen(request, timeout=15) as response:
        data = json.loads(response.read().decode("utf-8"))
    return data.get("matches", [])


def _country_by_code():
    return {country.code: country for country in Country.objects.all()}


def get_new_matches():
    """Partidos de la API que aún no están en la BD.

    Se omiten los que tengan algún equipo cuyo `code` no exista en Country.
    """
    countries = _country_by_code()
    nuevos = []
    for item in fetch_api_matches():
        team_1 = countries.get(item.get("team1"))
        team_2 = countries.get(item.get("team2"))
        if team_1 is None or team_2 is None:
            continue

        fecha = parse_datetime(item.get("date"), item.get("time"))
        if Match.objects.filter(team_1=team_1, team_2=team_2, date=fecha).exists():
            continue

        nuevos.append(
            {
                "team_1": team_1,
                "team_2": team_2,
                "stage": item.get("group") or item.get("round") or "",
                "date": fecha,
                "ground": item.get("ground") or None,
            }
        )
    return nuevos


def create_matches(nuevos):
    for n in nuevos:
        Match.objects.create(
            team_1=n["team_1"],
            team_2=n["team_2"],
            stage=n["stage"],
            date=n["date"],
            ground=n["ground"],
        )
    return len(nuevos)


def update_results_from_api():
    """Actualiza los goles de los partidos locales con el score.ft de la API.

    En score.ft el primer número son los goles del team_1 y el segundo los del
    team_2. Devuelve cuántos partidos se actualizaron.
    """
    countries = _country_by_code()
    actualizados = 0
    for item in fetch_api_matches():
        score = item.get("score") or {}
        ft = score.get("ft")
        if not ft or len(ft) < 2:
            continue

        team_1 = countries.get(item.get("team1"))
        team_2 = countries.get(item.get("team2"))
        if team_1 is None or team_2 is None:
            continue

        fecha = parse_datetime(item.get("date"), item.get("time"))
        try:
            match = Match.objects.get(team_1=team_1, team_2=team_2, date=fecha)
        except Match.DoesNotExist:
            continue

        goals_1, goals_2 = ft[0], ft[1]
        # Penales (si el partido se definió en la tanda).
        penalties = score.get("p")
        if penalties and len(penalties) >= 2:
            pen_1, pen_2 = penalties[0], penalties[1]
        else:
            pen_1, pen_2 = None, None

        if (
            match.goals_team_1 != goals_1
            or match.goals_team_2 != goals_2
            or match.penalties_team_1 != pen_1
            or match.penalties_team_2 != pen_2
        ):
            match.goals_team_1 = goals_1
            match.goals_team_2 = goals_2
            match.penalties_team_1 = pen_1
            match.penalties_team_2 = pen_2
            match.save(
                update_fields=[
                    "goals_team_1",
                    "goals_team_2",
                    "penalties_team_1",
                    "penalties_team_2",
                ]
            )
            actualizados += 1

    return actualizados
