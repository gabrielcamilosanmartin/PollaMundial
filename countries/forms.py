from django import forms

from common.forms import TailwindFormMixin

from .models import Country

COUNTRY_FIELDS = ("name", "code")


class CountryCreateForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Country
        fields = COUNTRY_FIELDS


class CountryUpdateForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Country
        fields = COUNTRY_FIELDS
