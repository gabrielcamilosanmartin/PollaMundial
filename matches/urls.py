from django.urls import path

from . import views

urlpatterns = [
    path("administrar/partidos/", views.MatchListView.as_view(), name="match_list"),
    path(
        "administrar/partidos/sincronizar/",
        views.MatchSyncView.as_view(),
        name="match_sync",
    ),
    path(
        "administrar/partidos/nuevo/",
        views.MatchCreateView.as_view(),
        name="match_create",
    ),
    path(
        "administrar/partidos/<int:pk>/editar/",
        views.MatchUpdateView.as_view(),
        name="match_update",
    ),
    path(
        "administrar/partidos/<int:pk>/eliminar/",
        views.MatchDeleteView.as_view(),
        name="match_delete",
    ),
]
