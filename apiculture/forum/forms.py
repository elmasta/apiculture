from django import forms
from .models import Post
from django_summernote.widgets import SummernoteWidget


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "categories"]
        widgets = {
            "content": SummernoteWidget(attrs={"class": "form-control"}),
        }


class Reply(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content"]
        widgets = {
            "content": SummernoteWidget(attrs={"class": "form-control"}),
        }
