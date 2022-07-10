from django.contrib import admin
from forum.models import Category, Post, Reply, Member, Banned_IP

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Reply)
admin.site.register(Member)
admin.site.register(Banned_IP)
