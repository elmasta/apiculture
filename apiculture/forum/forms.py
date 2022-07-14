from django import forms
from .models import Reply, Post, Category, Member
from django_summernote.widgets import SummernoteWidget


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "categories"]
        widgets = {
            "content": SummernoteWidget(attrs={"class": "form-control"}),
        }


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ["content"]
        widgets = {
            "content": SummernoteWidget(attrs={"class": "form-control"}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["title", "description"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "id": "titleDesc"}),
            "description": forms.TextInput(attrs={"class": "form-control", "id": "description"}),
        }
