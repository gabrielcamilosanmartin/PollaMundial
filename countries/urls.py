from django.urls import path

from . import views

urlpatterns = [
    path("administrar/paises/", views.CountryListView.as_view(), name="country_list"),
    path(
        "administrar/paises/nuevo/",
        views.CountryCreateView.as_view(),
        name="country_create",
    ),
    path(
        "administrar/paises/<int:pk>/editar/",
        views.CountryUpdateView.as_view(),
        name="country_update",
    ),
    path(
        "administrar/paises/<int:pk>/eliminar/",
        views.CountryDeleteView.as_view(),
        name="country_delete",
    ),
]
