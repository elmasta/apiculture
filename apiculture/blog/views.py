from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from blog.models import *
from blog.forms import *

def index(request):

    context = {}
    if request.user.is_authenticated:
        return render(
            request, 'blog/index.html')
    return render(request, 'blog/index.html')

def login_page(request):

    context = {}
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            if User.objects.filter(username=username).exists():
                user = authenticate(username=username,
                                    password=password)
                if user is not None:
                    login(request, user)
                    request.session['context'] = {}
                    return redirect("index")
                context["errors"] = "Mot de passe invalide"
            else:
                context["errors"] = "Ce pseudo est inconnu"
    form = UserLoginForm()
    context["form"] = form
    return render(request, "blog/login.html", context)

def user_logout(request):
    """view used to logout the user"""

    if request.user.is_authenticated:
        logout(request)
    return redirect("index")

def cours(request, cours_id):

    context = {}
    current_cours = Cours.objects.get(id=cours_id)
    context = {"cours" : current_cours}
    return render(request, 'blog/cours.html', context)

def cours_index(request):
    
    context = {}
    if request.user.is_authenticated:
        if request.method == "POST":
            None
    cours = Cours.objects.all()
    context["list"] = cours
    return render(request, 'blog/cours_index.html', context)

def cours_creation(request):
    
    context = {}
    if request.user.is_authenticated:
        if request.method == "POST":
            form = CreationCoursForm(request.POST)
            if form.is_valid():
                new_cours = Cours(
                    name = form.cleaned_data["name"],
                    teatching = form.cleaned_data["teatching"],
                    description = form.cleaned_data["description"]
                )
                new_cours.save()
                return redirect("cours_index")
        form = CreationCoursForm()
        context["form"] = form
        return render(request, 'blog/coursedit.html', context)
    return redirect("index")

def forum(request):
    return render(request, 'blog/index.html')

def shop(request):
    return render(request, 'blog/index.html')