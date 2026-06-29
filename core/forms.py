from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import BaseUserCreationForm

User = get_user_model()

# Campos editables en el CRUD de usuarios (el email es el identificador).
USER_FIELDS = ("email", "first_name", "last_name", "is_active", "is_staff")

INPUT_CLASS = (
    "block w-full rounded-lg border border-slate-300 bg-white px-3.5 py-2.5 text-sm "
    "text-slate-900 placeholder-slate-400 shadow-sm transition "
    "focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/30 focus:outline-none"
)
CHECKBOX_CLASS = (
    "h-4 w-4 rounded border-slate-300 text-emerald-600 focus:ring-emerald-500/40"
)


class TailwindFormMixin:
    """Aplica clases de Tailwind a todos los campos del formulario."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault("class", CHECKBOX_CLASS)
            else:
                field.widget.attrs.setdefault("class", INPUT_CLASS)


class UserCreateForm(TailwindFormMixin, BaseUserCreationForm):
    class Meta:
        model = User
        fields = USER_FIELDS


class UserUpdateForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = USER_FIELDS
