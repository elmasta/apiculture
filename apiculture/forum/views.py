from django.shortcuts import redirect, render, get_object_or_404
from forum.models import Category, Post, Reply
from forum.utils import update_views
from forum.forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def forum(request):
    forums = Category.objects.all()
    num_posts = Post.objects.all().count()
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
        "title": "OZONE forum app"
    }
    return render(request, "forum/forums.html", context)


@login_required
def detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_authenticated:
        author = User.objects.get(user=request.user)
    if "reply-form" in request.POST:
        reply = request.POST.get("reply")
        new_reply, created = Reply.objects.get_or_create(
            user=author, content=reply)
    context = {
        "post": post,
        "title": "OZONE: " + post.title,
    }
    update_views(request, post)
    return render(request, "forum/detail.html", context)


def posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(approved=True, categories=category)
    paginator = Paginator(posts, 5)
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        "posts": posts,
        "forum": category,
        "title": "OZONE: Posts"
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


def latest_posts(request):
    posts = Post.objects.all().filter(approved=True)[:10]
    context = {
        "posts": posts,
        "title": "OZONE: Les 10 derniers topic."
    }

    return render(request, "forum/latest-posts.html", context)


def search_result(request):

    return render(request, "forum/search.html")
