from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
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
