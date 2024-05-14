from django.urls import path,include

from .views import ProductListView

urlpatterns = [
    path('products/', ProductListView.as_view(), name="products_list_search"),
    path("",include("cart.api.urls")),
]