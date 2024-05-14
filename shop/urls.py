from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("shop/", views.ShopView.as_view(), name="shop"),
    path("shop/<str:category_slug>/", views.CategoryRedirectView.as_view(), name="category_redirect"),
]
