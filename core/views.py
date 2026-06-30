from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from common.mixins import StaffRequiredMixin

from .forms import UserCreateForm, UserUpdateForm

User = get_user_model()


class UserListView(StaffRequiredMixin, ListView):
    model = User
    template_name = "core/user_list.html"
    context_object_name = "users"
    ordering = ["email"]


class UserCreateView(StaffRequiredMixin, CreateView):
    model = User
    form_class = UserCreateForm
    template_name = "core/user_form.html"
    success_url = reverse_lazy("user_list")
    extra_context = {"title": "Crear usuario"}

    def form_valid(self, form):
        # Los usuarios creados por el admin deben definir su contraseña al
        # iniciar sesión por primera vez.
        response = super().form_valid(form)
        self.object.must_change_password = True
        self.object.save(update_fields=["must_change_password"])
        return response


class UserUpdateView(StaffRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "core/user_form.html"
    success_url = reverse_lazy("user_list")
    extra_context = {"title": "Editar usuario"}


class UserDeleteView(StaffRequiredMixin, DeleteView):
    model = User
    template_name = "core/user_confirm_delete.html"
    success_url = reverse_lazy("user_list")


class UserResetLinkView(StaffRequiredMixin, View):
    """Genera el enlace de restablecer contraseña de un usuario (sin enviar correo).

    Devuelve el mismo enlace que iría en el email, para copiarlo y compartirlo
    manualmente. El enlace caduca a los 30 minutos y es de un solo uso.
    """

    def get(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        path = reverse(
            "password_reset_confirm", kwargs={"uidb64": uid, "token": token}
        )
        return JsonResponse(
            {"url": request.build_absolute_uri(path), "email": user.email}
        )
