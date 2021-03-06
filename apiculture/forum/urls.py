from django.urls import path
from . import views

urlpatterns = [
    path("forum", views.forum, name="forum"),
    path("detail/<slug>/", views.detail, name="detail"),
    path("posts/<slug>/", views.posts, name="posts"),
    path("create_post", views.create_post, name="create_post"),
    path("search", views.search_result, name="search_result"),
    path("admin", views.forum_admin, name="admin"),
    # not used
    # path("latest_posts", views.latest_posts, name="latest_posts"),
]