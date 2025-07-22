from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        help_text="Enter your Amteck email address."
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        help_text="Same password used to log into your computer."
    )