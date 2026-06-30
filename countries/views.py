from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from common.mixins import StaffRequiredMixin

from .forms import CountryCreateForm, CountryUpdateForm
from .models import Country


class CountryListView(StaffRequiredMixin, ListView):
    model = Country
    template_name = "countries/country_list.html"
    context_object_name = "countries"
    ordering = ["name"]


class CountryCreateView(StaffRequiredMixin, CreateView):
    model = Country
    form_class = CountryCreateForm
    template_name = "countries/country_form.html"
    success_url = reverse_lazy("country_list")
    extra_context = {"title": "Crear país"}


class CountryUpdateView(StaffRequiredMixin, UpdateView):
    model = Country
    form_class = CountryUpdateForm
    template_name = "countries/country_form.html"
    success_url = reverse_lazy("country_list")
    extra_context = {"title": "Editar país"}


class CountryDeleteView(StaffRequiredMixin, DeleteView):
    model = Country
    template_name = "countries/country_confirm_delete.html"
    success_url = reverse_lazy("country_list")
