from blog.models import *
from django.contrib.auth.models import User
from django import forms


class UserLoginForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control"}))

class CreationCoursForm(forms.ModelForm):

    class Meta:
        model = Cours
        fields = ["name", "teatching", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "teatching": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
        }
