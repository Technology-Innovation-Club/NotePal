from django.urls import path
from .views import signup, login, chat, landing_page

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", login, name="login"),
    path("chat/", chat, name="chat"),
    path("", landing_page, name="landing_page"),
]
