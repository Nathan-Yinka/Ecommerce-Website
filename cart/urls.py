from django.urls import path
from . import views

urlpatterns = [
    path('',views.CartAddView.as_view()),
]