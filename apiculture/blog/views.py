import forum.func as func
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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
                    return redirect("login")
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


@login_required
def event_admin(request):

    if request.user.is_superuser:
        if request.method == "POST":
            if request.POST.get("delete"):
                Event.objects.get(id=request.POST.get("delete")).delete()
            elif request.POST.get("published"):
                modif_event = Event.objects.get(id=request.POST.get("published"))
                modif_event.published = True
                modif_event.save()
            elif request.POST.get("unpublished"):
                modif_event = Event.objects.get(id=request.POST.get("unpublished"))
                modif_event.published = False
                modif_event.save()
        events = Event.objects.all()
        context = {"events" : events}
        return render(request, 'blog/event_admin.html', context)
    return redirect("index")


def cours(request, cours_id):

    context = {}
    current_cours = Cours.objects.get(id=cours_id)
    if request.user.is_superuser:
        if request.method == "POST":
            form = CreationCoursForm(request.POST)
            if form.is_valid():
                current_cours.name = form.cleaned_data["name"]
                current_cours.teatching = form.cleaned_data["teatching"]
                current_cours.description = form.cleaned_data["description"]
                if request.POST.get("publish"):
                    current_cours.published = True
                current_cours.save()
        form = CreationCoursForm(instance=current_cours)
        context["form"] = form
    context["cours"] = current_cours
    return render(request, 'blog/cours.html', context)


def cours_index(request):
    
    if request.user.is_authenticated and request.user.is_superuser:
        cours = Cours.objects.all().order_by("created_at")
        if request.method == "POST":
            if request.POST.get("delete"):
                Cours.objects.get(id=request.POST.get("delete")).delete()
            elif request.POST.get("published"):
                modif_cours = Cours.objects.get(id=request.POST.get("published"))
                modif_cours.published = True
                modif_cours.save()
            elif request.POST.get("unpublished"):
                modif_cours = Cours.objects.get(id=request.POST.get("unpublished"))
                modif_cours.published = False
                modif_cours.save()
    else:
        cours = Cours.objects.exclude(published=False).order_by("created_at")
    context = {"list": cours}
    return render(request, 'blog/cours_index.html', context)


@login_required
def cours_creation(request):
    
    if request.user.is_superuser:
        if request.method == "POST":
            form = CreationCoursForm(request.POST)
            if form.is_valid() and request.POST.get("register"):
                new_cours = Cours(
                    name = form.cleaned_data["name"],
                    teatching = form.cleaned_data["teatching"],
                    description = form.cleaned_data["description"]
                )
                new_cours.save()
            elif form.is_valid() and request.POST.get("publish"):
                new_cours = Cours(
                    name = form.cleaned_data["name"],
                    teatching = form.cleaned_data["teatching"],
                    description = form.cleaned_data["description"],
                    published = True
                )
            return redirect("cours_index")
        form = CreationCoursForm()
        context = {"form": form}
        return render(request, 'blog/coursedit.html', context)
    return redirect("index")


@login_required
def event_creation(request):

    if request.user.is_superuser:
        if request.method == "POST":
            form = EventForm(request.POST)
            if form.is_valid():
                if request.POST.get("publish"):
                    new_event = Event(
                        name = form.cleaned_data["name"],
                        description = form.cleaned_data["description"],
                        published = True
                    )
                else:
                    new_event = Event(
                        name = form.cleaned_data["name"],
                        description = form.cleaned_data["description"]
                    )
                new_event.save()
            return redirect("event_admin")
        form = EventForm()
        context = {"form": form}
        return render(request, 'blog/event_creation.html', context)
    return redirect("index")


@login_required
def event_modif(request, event_id):

    if request.user.is_superuser:
        current_event = Event.objects.get(id=event_id)
        if request.method == "POST":
            form = EventForm(request.POST)
            if form.is_valid():
                current_event.name = form.cleaned_data["name"]
                current_event.description = form.cleaned_data["description"]
                if request.POST.get("publish"):
                    current_event.published = True
                current_event.save()
                return redirect("event_admin")
        form = EventForm(instance=current_event)
        context = {"form": form}
        return render(request, 'blog/event_creation.html', context)
    return redirect("index")


@login_required
def index_modif(request):

    if request.user.is_superuser:
        introduction = Introduction.objects.all()
        introduction = introduction[0]
        description = Description.objects.all()
        description = description[0]
        if request.method == "POST":
            form_intro = IntroductionForm(request.POST)
            form_desc = DescriptionForm(request.POST)
            if form_intro.is_valid():
                introduction.description = form_intro.cleaned_data["description"]
                introduction.save()
            elif form_desc.is_valid():
                description.description = form_desc.cleaned_data["description"]
                description.save()
            return redirect("index")
        form_intro = IntroductionForm(instance=introduction)
        form_desc = DescriptionForm(instance=description)
        context = {
            "form_intro": form_intro,
            "form_desc": form_desc,
        }
        return render(request, 'blog/index_modif.html', context)
    return redirect("index")


def legal(request):

    
    return render(request, 'blog/legal.html')
