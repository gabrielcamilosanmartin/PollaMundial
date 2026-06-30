from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import BaseUserCreationForm

from common.forms import TailwindFormMixin

User = get_user_model()

# Campos editables en el CRUD de usuarios (el email es el identificador).
USER_FIELDS = ("email", "first_name", "last_name", "is_active", "is_staff")


class UserCreateForm(TailwindFormMixin, BaseUserCreationForm):
    class Meta:
        model = User
        fields = USER_FIELDS


class UserUpdateForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = USER_FIELDS
