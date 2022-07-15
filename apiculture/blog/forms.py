from blog.models import *
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
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
            "teatching": SummernoteWidget(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
        }

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": SummernoteWidget(attrs={"class": "form-control"}),
        }

class PasswordChange(forms.Form):

    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control"}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control"}))
    new_password_comf = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control"}))


class UserDelete(forms.Form):

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control"}))

class IntroductionForm(forms.ModelForm):

    class Meta:
        model = Introduction
        fields = ["description"]
        widgets = { 
            "description": SummernoteWidget(attrs={"class": "form-control"})
        }

class DescriptionForm(forms.ModelForm):

    class Meta:
        model = Description
        fields = ["description"]
        widgets = { 
            "description": SummernoteWidget(attrs={"class": "form-control"})
        }
