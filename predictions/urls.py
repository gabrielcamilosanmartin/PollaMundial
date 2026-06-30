from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("predicciones/", views.MyPredictionsView.as_view(), name="my_predictions"),
    path("resultados/", views.ResultsView.as_view(), name="results"),
    # Administrar > Predicciones (backfill por partido, solo staff)
    path(
        "administrar/predicciones/",
        views.PredictionAdminListView.as_view(),
        name="prediction_admin_list",
    ),
    path(
        "administrar/predicciones/<int:pk>/",
        views.PredictionMatchEditView.as_view(),
        name="prediction_admin_match",
    ),
]
