from django.urls import path
from . import views
from django.views.defaults import page_not_found

urlpatterns = [
    path('password/reset/done/', views.MyEmailVerificationSentView.as_view(), name='account_reset_password_done'),
    path('confirm-email/', views.MyEmailVerificationSentView.as_view(), name='account_email_verification_sent'),
    path("password/reset/key/done/", views.MyEmailVerificationSentView.as_view(),name="account_reset_password_from_key_done"),
    path("reauthenticate/", page_not_found, {'exception': Exception()}, name="account_reauthenticate"),
    path("email/", page_not_found, {'exception': Exception()}),
]
