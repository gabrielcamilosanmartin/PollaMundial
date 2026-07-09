from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import BaseUserCreationForm

from common.forms import TailwindFormMixin

User = get_user_model()

# Campos editables en el CRUD de usuarios (el username es el identificador).
USER_FIELDS = ("username", "first_name", "last_name", "email", "is_active", "is_staff")


class UserCreateForm(TailwindFormMixin, BaseUserCreationForm):
    class Meta:
        model = User
        fields = USER_FIELDS


class UserUpdateForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = USER_FIELDS
