from django.urls import path
from .views import signup, login_user, logout_user

urlpatterns = [
    path("login/", login_user, name="custom_login"),
    path("signup/", signup, name="custom_signup"),
    path("logout/", logout_user, name="custom_logout"),
]
