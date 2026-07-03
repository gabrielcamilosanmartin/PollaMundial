import zoneinfo

from django.utils import timezone


class TimezoneMiddleware:
    """Activa la zona horaria del usuario a partir de la cookie 'tz'.

    El navegador guarda su zona horaria (IANA, p. ej. 'America/Bogota') en esa
    cookie. Así, cálculos como "el inicio del día de hoy" usan la fecha local
    del usuario y no la del servidor (UTC).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.COOKIES.get("tz")
        if tzname:
            try:
                timezone.activate(zoneinfo.ZoneInfo(tzname))
            except Exception:  # noqa: BLE001 - zona inválida: usamos la de por defecto
                timezone.deactivate()
        else:
            timezone.deactivate()
        return self.get_response(request)
