import os
import forum.func as func
from django.shortcuts import render, get_list_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from blog.models import *
from blog.forms import *
from forum.models import Member, Banned_IP


def index(request):

    introductions = Introduction.objects.all()
    descriptions = Description.objects.all()
    events = Event.objects.filter(published=True).order_by("-created_at")
    context = {
        "introductions": introductions,
        "descriptions": descriptions,
        "events": events,
    }
    return render(request, 'blog/index.html', context)


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


def user_signin(request):

    context = {}
    ip_client = func.get_client_ip(request)
    try:
        Banned_IP.objects.get(ip=ip_client)
        return redirect("index")
    except:
        if request.user.is_authenticated:
            return redirect("index")
        if request.method == "POST":
            form = UserLoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                if User.objects.filter(username=username).exists():
                    context["errors"] = "Cet utilisateur existe déjà"
                else:
                    User.objects.create_user(
                    username=username,
                    password=password,
                    is_active=True)
                    new_user = User.objects.get(username=username)
                    new_member = Member(
                    user = new_user,
                    ip = ip_client,
                    is_moderator = False,
                    is_banned = False
                    )
                    new_member.save()
                    return redirect("login_page")
        form = UserLoginForm()
        context["form"] = form
        return render(request, "blog/signin.html", context)


def user_logout(request):
    """view used to logout the user"""

    if request.user.is_authenticated:
        logout(request)
    return redirect("index")


def user_option(request):

    if request.user.is_authenticated:
        if request.method == "POST":
            if request.POST.get("delete") is None:
                form = PasswordChange(request.POST)
                if form.is_valid() and\
                   form.cleaned_data["new_password_comf"] ==\
                   form.cleaned_data["new_password"] and\
                   authenticate(username=request.user.username,
                                password=request.POST.get("old_password")):
                    user = User.objects.get(id=request.user.id)
                    user.set_password(form.cleaned_data["new_password_comf"])
                    user.save()
            elif authenticate(username=request.user.username,
                              password=request.POST.get("password"))\
                              is not None:
                User.objects.get(id=request.user.id).delete()
                return redirect("index")
        pass_form = PasswordChange()
        del_form = UserDelete()
        context = {
            "pass_form": pass_form,
            "del_form": del_form,
        }
        return render(request, "blog/user.html", context)
    else:
        return redirect("index")


def event_admin(request):

    return redirect("index")


def cours(request, cours_id):

    current_cours = Cours.objects.get(id=cours_id)
    context = {"cours" : current_cours}
    return render(request, 'blog/cours.html', context)


def cours_index(request):
    
    context = {}
    if request.user.is_authenticated:
        if request.method == "POST":
            if request.POST.get("delete"):
                Cours.objects.get(id=request.POST.get("delete")).delete()
            elif request.POST.get("published"):
                modif_cours = Cours.objects.get(id=request.POST.get("published"))
                modif_cours.published = True
                modif_cours.save()
    if request.user.is_superuser:
        cours = Cours.objects.all().order_by("created_at")
    else:
        cours = Cours.objects.exclude(published=False).order_by("created_at")
    if cours:
        paginator = Paginator(cours, 1)
        page = request.GET.get('page')
        try:
            cours = paginator.page(page)
        except PageNotAnInteger:
            cours = paginator.page(1)
        except EmptyPage:
            cours = paginator.page(paginator.num_pages)
        context["list"] = cours
        return render(request, 'blog/cours_index.html', context)
    else:
        return redirect("index")


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
