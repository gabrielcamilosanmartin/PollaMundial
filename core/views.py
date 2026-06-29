from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import UserCreateForm, UserUpdateForm

User = get_user_model()


@login_required
def home(request):
    return render(request, "core/home.html")


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Solo personal autorizado (is_staff) puede gestionar usuarios."""

    def test_func(self):
        return self.request.user.is_staff


class UserListView(StaffRequiredMixin, ListView):
    model = User
    template_name = "core/user_list.html"
    context_object_name = "users"
    ordering = ["username"]


class UserCreateView(StaffRequiredMixin, CreateView):
    model = User
    form_class = UserCreateForm
    template_name = "core/user_form.html"
    success_url = reverse_lazy("user_list")
    extra_context = {"title": "Crear usuario"}


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
