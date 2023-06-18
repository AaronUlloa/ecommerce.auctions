from django import urls
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = "auctions"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("forget", views.forget, name="forget"),
    path("auction", views.addNewItem, name="auction"),
]
