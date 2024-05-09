from typing import Any
from django.shortcuts import render, redirect
from allauth.account.views import LoginView, EmailVerificationSentView


class MyEmailVerificationSentView(EmailVerificationSentView):

    def get(self, *args, **kwargs):
        return redirect('account_login')
