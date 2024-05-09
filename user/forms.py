from allauth.account.forms import SignupForm, LoginForm, ResetPasswordForm, ResetPasswordKeyForm, ChangePasswordForm, \
    SetPasswordForm
from django import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from myshop.utils import DivErrorList, DivErrorList2


class MyCustomSignupForm(SignupForm):
    username = forms.CharField(max_length=30, label='Username')
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')

    # Add more fields as needed

    def __init__(self, *args, **kwargs):
        super(MyCustomSignupForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })
        self.error_class = DivErrorList

    def clean_username(self):
        username = self.cleaned_data['username']
        # Check if the username already exists in the database
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose a different one.")
        return username

    def save(self, request):
        # Call the parent class's save() method to perform the default signup process
        user = super(MyCustomSignupForm, self).save(request)

        # Save additional form data to the user object
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        # Save more additional fields here

        user.save()  # Save the user object with the additional data

        return user


class MyCustomLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super(MyCustomLoginForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })
        self.error_class = DivErrorList2

    error_messages = {
        "account_inactive": _("This account is currently inactive."),
        "email_password_mismatch": _(
            "Invaild Credential Was Entered"
        ),
        "username_password_mismatch": _(
            "Invaild Credential Was Entered"
        ),
    }


class MyCustomResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(MyCustomResetPasswordForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })
        self.error_class = DivErrorList2

    def save(self, request, *args, **kwargs):
        email_address = super(MyCustomResetPasswordForm, self).save(request, **kwargs)
        messages.success(request, f"Password Reset Mail Sent Successfully to {email_address}")
        return email_address


class MyCustomResetPasswordKeyForm(ResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super(MyCustomResetPasswordKeyForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })
        self.error_class = DivErrorList2

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error("password1", _("The two passwords must match"))
        return self.cleaned_data


class MyCustomChangePasswordForm(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super(MyCustomChangePasswordForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })
        self.error_class = DivErrorList2

    def clean_oldpassword(self):
        if not self.user.check_password(self.cleaned_data.get("oldpassword")):
            raise forms.ValidationError(
                "The old password is incorrect. Try again"
            )
        return self.cleaned_data["oldpassword"]


class MyCustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(MyCustomSetPasswordForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })
        self.error_class = DivErrorList2
