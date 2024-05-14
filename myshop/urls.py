from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('user.urls')),
    path('accounts/', include('allauth.urls')),
    path("", include("shop.urls", namespace="shop")),
    path("api/", include("shop.api.urls")),
    path("cart", include("cart.urls")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
