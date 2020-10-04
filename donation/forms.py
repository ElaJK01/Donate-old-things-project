from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from donation.models import CustomUser


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'validate','placeholder': 'Email'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Hasło'}))


class RegisterForm(forms.Form):
    name = forms.CharField(widget=TextInput(attrs={'placeholder': 'Imię'}), label='')
    last_name = forms.CharField(widget=TextInput(attrs={'placeholder': 'Nazwisko'}), label='')
    email = forms.CharField(widget=TextInput(attrs={'placeholder': 'Email'}), label='')
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Hasło'}), label='')
    password2 = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Powtórz hasło'}), label='')

