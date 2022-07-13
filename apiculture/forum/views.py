from django.shortcuts import redirect, render, get_object_or_404, get_list_or_404
from forum.models import Category, Post, Reply, Banned_IP, Member
from forum.utils import update_views
from forum.forms import PostForm, ReplyForm
from forum.context_processors import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import forum.func as func


def forum(request):

    if request.user.is_authenticated:
        member = Member.objects.get(user=request.user.id)
    else:
        member = {"is_moderator": False}
    forums = Category.objects.all()
    num_posts = Post.objects.filter(approved=True).count()
    num_users = User.objects.all().count()
    num_categories = forums.count()
    ip_client = func.get_client_ip(request)
    try:
        Banned_IP.objects.get(ip=ip_client)
        return redirect("index")
    except:
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
            "title": "OZONE forum app"
        }
        return render(request, "forum/forums.html", context)


def detail(request, slug):

    topic = get_object_or_404(Post, slug=slug)
    if request.user.is_authenticated:
        member = Member.objects.get(user=request.user.id)
        if request.method == "POST":
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

    if request.user.is_authenticated:
        member = Member.objects.get(user=request.user.id)
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
        if form.is_valid():
            author = User.objects.get(user=request.user)
            new_post = form.save(commit=False)
            new_post.user = author
            new_post.save()
            form.save_m2m()
            return redirect("forum")
    context.update({
        "form": form,
        "title": "OZONE: Créez un nouveau topic."
    })
    return render(request, "forum/create_post.html", context)


def search_result(request):

    searchFunction(request)
    return render(request, "forum/search.html")


def forum_admin(request):

    return redirect("index")
