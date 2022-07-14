from turtle import title
from django.shortcuts import redirect, render, get_object_or_404, get_list_or_404
from django.utils.text import slugify
from forum.models import Category, Post, Reply, Banned_IP, Member
from forum.utils import update_views
from forum.forms import *
from forum.context_processors import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import forum.func as func


def forum(request):

    ip_client = func.get_client_ip(request)
    try:
        Banned_IP.objects.get(ip=ip_client)
        return redirect("index")
    except:
        form = None
        if request.user.is_authenticated:
            member = Member.objects.get(user=request.user.id)
            if member.is_moderator:
                form = CategoryForm(request.POST)
                if request.method == "POST":
                    if request.POST.get("delete"):
                        Category.objects.get(id=request.POST.get("delete")).delete()
                    elif form.is_valid():
                        new_category = Category(
                        title = form.cleaned_data["title"],
                        description = form.cleaned_data["description"]
                        )
                        new_category.save()
        else:
            member = {"is_moderator": False}
        forums = Category.objects.all()
        num_posts = Post.objects.filter(approved=True).count()
        num_users = User.objects.all().count()
        num_categories = forums.count()
        try:
            last_post = Post.objects.latest("date")
        except:
            last_post = []
        context = {
            "forums": forums,
            "num_posts": num_posts,
            "num_users": num_users,
            "num_categories": num_categories,
            "last_post": last_post,
            "member": member,
            "form": form,
            "title": "OZONE forum app"
        }
        return render(request, "forum/forums.html", context)


def detail(request, slug):

    ip_client = func.get_client_ip(request)
    try:
        Banned_IP.objects.get(ip=ip_client)
        return redirect("index")
    except:
        topic = get_object_or_404(Post, slug=slug)
        if request.user.is_authenticated:
            member = Member.objects.get(user=request.user.id)
            if request.method == "POST":
                if request.POST.get("delete") and member.is_moderator:
                    Reply.objects.get(id=request.POST.get("delete")).delete()
                else:
                    form = ReplyForm(request.POST)
                    if form.is_valid():
                        new_reply = Reply(
                        post = topic,
                        user = member,
                        content = form.cleaned_data["content"]
                        )
                        new_reply.save()
        else:
            member = {"is_moderator": False}
        form = ReplyForm()
        replies = Reply.objects.filter(post=topic.id).order_by("date")
        paginator = Paginator(replies, 10)
        page = request.GET.get('page')
        replies = paginator.get_page(page)
        context = {
            "category": topic.categories.title,
            "post": topic,
            "replies": replies,
            "title": "OZONE: " + topic.title,
            "form": form,
            "member": member,
        }
        update_views(request, topic)
        return render(request, "forum/detail.html", context)


def posts(request, slug):

    ip_client = func.get_client_ip(request)
    try:
        Banned_IP.objects.get(ip=ip_client)
        return redirect("index")
    except:
        if request.user.is_authenticated:
            member = Member.objects.get(user=request.user.id)
            if member.is_moderator and request.method == "POST":
                if request.POST.get("delete"):
                    Post.objects.get(id=request.POST.get("delete")).delete()
                elif request.POST.get("close"):
                    post = Post.objects.get(id=request.POST.get("close"))
                    post.closed = True
                    post.save()
                elif request.POST.get("open"):
                    post = Post.objects.get(id=request.POST.get("open"))
                    post.closed = False
                    post.save()
        else:
            member = {"is_moderator": False}
        category = get_object_or_404(Category, slug=slug)
        posts = Post.objects.filter(approved=True, categories=category).order_by('date')
        for i in posts:
            i.num_comments = len(Reply.objects.filter(post=i.id))
        paginator = Paginator(posts, 10)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
        context = {
            "posts": posts,
            "forum": category,
            "member": member,
            "title": "OZONE: Posts",
        }
        return render(request, "forum/posts.html", context)


@login_required
def create_post(request):
    context = {}
    form = PostForm(request.POST or None)
    if request.method == "POST":
        member = Member.objects.get(user=request.user.id)
        if form.is_valid():
            in_category = get_object_or_404(
                Category, slug=slugify(form.cleaned_data["categories"])
                )
            new_post = Post(
                    title = form.cleaned_data["title"],
                    user = member,
                    content = form.cleaned_data["content"],
                    categories = in_category
                )
            new_post.save()
            return redirect("forum")
    context.update({
        "form": form,
        "title": "OZONE: Créez un nouveau sujet."
    })
    return render(request, "forum/create_post.html", context)


def search_result(request):

    ip_client = func.get_client_ip(request)
    try:
        Banned_IP.objects.get(ip=ip_client)
        return redirect("index")
    except:
        search_context = searchFunction(request)
        paginator = Paginator(search_context["objects"], 10)
        page = request.GET.get('page')
        objects = paginator.get_page(page)
        context = {
            "objects": objects,
            "query": search_context["query"],
        }
        return render(request, "forum/search.html", context)


@login_required
def forum_admin(request):

    member = Member.objects.get(user=request.user.id)
    if member.is_moderator:
        if request.method == "POST":
            if request.POST.get("change"):
                member = Member.objects.get(user=request.POST.get("change"))
                if request.POST.get('moderator') == "on":
                    member.is_moderator = True
                    member.is_banned = False
                else:
                    member.is_moderator = False
                if request.POST.get('banned') == "on":
                    member.is_banned = True
                    member.is_moderator = False
                    ban_ip = Banned_IP(ip=member.ip)
                    ban_ip.save()
                else:
                    member.is_banned = False
                    Banned_IP.objects.get(ip=member.ip).delete()
                member.save()
                print(type(request.POST.get('moderator')))
                print(member.user.username)
        members = Member.objects.filter(user__isnull=False).order_by("user__username")
        context = {
            "members": members,
        }
        return render(request, "forum/forum_admin.html", context)
    return redirect("index")
