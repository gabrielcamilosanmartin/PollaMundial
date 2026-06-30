from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("predicciones/", views.MyPredictionsView.as_view(), name="my_predictions"),
    path("resultados/", views.ResultsView.as_view(), name="results"),
]
