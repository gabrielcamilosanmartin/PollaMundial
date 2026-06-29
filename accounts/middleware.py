from django.shortcuts import redirect
from django.urls import reverse


class ForcePasswordChangeMiddleware:
    """Obliga a los usuarios con must_change_password=True a definir su contraseña.

    Mientras el flag esté activo, cualquier petición se redirige a la página de
    cambio de contraseña inicial (salvo esa misma página, el logout y el cambio
    de idioma).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)
        if (
            user is not None
            and user.is_authenticated
            and getattr(user, "must_change_password", False)
        ):
            allowed = {
                reverse("initial_password_change"),
                reverse("logout"),
                reverse("set_language"),
            }
            if request.path not in allowed and not request.path.startswith("/static/"):
                return redirect("initial_password_change")

        return self.get_response(request)
