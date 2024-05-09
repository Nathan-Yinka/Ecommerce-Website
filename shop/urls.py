from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("", views.ProductListView.as_view(), name="products_list"),
]
