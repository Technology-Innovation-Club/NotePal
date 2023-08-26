from django.urls import path
from .views import signup, login, landing_page, forgot_password

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", login, name="login"),
    path("recover/", forgot_password, name="forgot_password"),
    path("", landing_page, name="landing_page"),
]
