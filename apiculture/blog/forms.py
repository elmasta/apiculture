from blog.models import *
from django.contrib.auth.models import User
from django import forms

class UserCreationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "password"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
        }

class UserLoginForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control"}))

class CreationCours(forms.Form):

    class Meta:
        model = Cours
        fields = ["name", "teatching", "description"]
        widgets = {
            "name": forms.CharField(attrs={"class": "form-control"}),
            "teatching": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control"})
        }
