from django.urls import path
from . import views

app_name = "auctions"

urlpatterns = [
    path("", views.item_list, name="item_list"),
    path("create_item/", views.create_item, name="create_item"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("forget", views.forget, name="forget"),
]
