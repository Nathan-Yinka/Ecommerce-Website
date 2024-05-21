from django.urls import path

from .views import CartGetAddApiView,CartProductDeleteApiView,WishlistAddRemoveGetApiView

urlpatterns = [
    path('cart/', CartGetAddApiView.as_view(), name="cart_fetch_add"),
    path("cart/delete/", CartProductDeleteApiView.as_view(), name="cart_delete"),

    path("wishlist/", WishlistAddRemoveGetApiView.as_view(), name="wishlist_fetch_add"),
]