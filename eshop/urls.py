# app urls **
from django.urls import path
from . import views

# app name **
app_name = 'eshop'

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # new paths **
    path("add", views.add, name="add"),
    path("listing=<int:listing_id>", views.listing, name="listing"),
    path("categories", views.categories, name="categories"),
    path("category=<str:category>", views.category, name="category"),
    path("comment=<int:listing_id>", views.comment, name="comment"),
    path("search", views.search, name="search"),
    path("cart", views.cart, name="cart"),
    path("checkout", views.checkout, name="checkout"),
    path("order=<int:order_id>", views.order, name="order"),
    path("orders", views.orders, name="orders"),
    path("profile=<str:username>", views.profile, name="profile")
]