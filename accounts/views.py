from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView


class InitialPasswordChangeView(LoginRequiredMixin, FormView):
    """El usuario define su contraseña en el primer inicio de sesión."""

    template_name = "registration/initial_password_change.html"
    form_class = SetPasswordForm
    success_url = reverse_lazy("home")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        user = form.user
        user.must_change_password = False
        user.save(update_fields=["must_change_password"])
        # Evita que el cambio de contraseña cierre la sesión actual.
        update_session_auth_hash(self.request, user)
        return super().form_valid(form)
