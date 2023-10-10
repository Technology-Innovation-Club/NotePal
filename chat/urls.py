from django.urls import path
from .views import chat, create_demo_user

urlpatterns = [
    path("demo/", create_demo_user, name="demo_user"),
    path("", chat, name="chat"),
]
