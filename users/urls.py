from django.urls import path
from .views import (
    SignUpView,
    ProfileDetailView,
    ProfileUpdateView,
    AccountDeleteView,
    ProfileListView,
    ProfileDeleteView
)

app_name = "users"

urlpatterns = [
    # registro
    path("signup/", SignUpView.as_view(), name="signup"),

    # detalle de perfil
    path(
        "profile/<str:username>/",
        ProfileDetailView.as_view(),
        name="profile_detail",
    ),

    # editar perfil (sólo el dueño)
    path(
        "profile/<str:username>/edit/",
        ProfileUpdateView.as_view(),
        name="profile_edit",
    ),

    # eliminar cuenta (sólo el dueño)
    path(
        "account/delete/",
        AccountDeleteView.as_view(),
        name="account_delete",
    ),
    path("profiles/",                 ProfileListView.as_view(),   name="profile_list"),
    path("profiles/<int:pk>/delete/", ProfileDeleteView.as_view(), name="profile_delete"),
]