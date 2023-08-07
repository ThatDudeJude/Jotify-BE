from django.urls import path
from .views import (
    signup,
    login_user,
    logout_user,
    reset_password,
    confirm_password_reset,
)

urlpatterns = [
    path("login/", login_user, name="custom_login"),
    path("signup/", signup, name="custom_signup"),
    path("logout/", logout_user, name="custom_logout"),
    path("password-reset/", reset_password, name="custom_password_reset"),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        confirm_password_reset,
        name="confirm_password_reset",
    ),
]
