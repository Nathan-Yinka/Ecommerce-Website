from django.urls import path

from .views import CartGetAddApiView,CartProductDeleteApiView

urlpatterns = [
    path('cart/', CartGetAddApiView.as_view(), name="cart_fetch_add"),
    path("cart/delete/", CartProductDeleteApiView.as_view(), name="cart_delete"),
]