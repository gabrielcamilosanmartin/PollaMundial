from django.urls import path

from . import views

urlpatterns = [
    # Administrar > Usuarios (CRUD)
    path("administrar/usuarios/", views.UserListView.as_view(), name="user_list"),
    path(
        "administrar/usuarios/nuevo/",
        views.UserCreateView.as_view(),
        name="user_create",
    ),
    path(
        "administrar/usuarios/<int:pk>/editar/",
        views.UserUpdateView.as_view(),
        name="user_update",
    ),
    path(
        "administrar/usuarios/<int:pk>/eliminar/",
        views.UserDeleteView.as_view(),
        name="user_delete",
    ),
    path(
        "administrar/usuarios/<int:pk>/enlace-reset/",
        views.UserResetLinkView.as_view(),
        name="user_reset_link",
    ),
]
