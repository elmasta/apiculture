from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse


def index(request):
    return render(request, 'blog/index.html')

def forum(request):
    return render(request, 'blog/index.html')

def shop(request):
    return render(request, 'blog/index.html')

def cours(request):
    
    if request.user.is_authenticated:
        if request.method == "POST":
            None
    return redirect("index")