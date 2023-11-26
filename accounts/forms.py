from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from accounts.models import User


class SignupForm(UserCreationForm):
    access_key = forms.CharField(max_length=100)
    secret_key = forms.CharField(max_length=100)
    bot_token = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ("username", "email", "access_key", "secret_key", "bot_token")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.access_key = self.cleaned_data["access_key"]
        user.secret_key = self.cleaned_data["secret_key"]
        user.bot_token = self.cleaned_data["bot_token"]
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    pass
