"""apiculture URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from django.contrib import admin
from django.urls import path
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.user_logout, name='user_logout'),
    path('forum/', views.forum, name="forum"),
    path('shop/', views.shop, name="shop"),
    path('cours/<int:cours_id>', views.cours, name="cours"),
    path('cours_index/', views.cours_index, name="cours_index"),
    path('cours_creation/', views.cours_creation, name="cours_creation")
    # path admin to be changed in prod:
    # path(str(os.getenv("ADMIN_LINK")), admin.site.urls)
]
