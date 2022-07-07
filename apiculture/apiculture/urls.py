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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from blog import views

urlpatterns = [
    path('', views.index, name="index"),
    path('blog/', include('blog.urls')),
    path('forum/', include('forum.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('hitcount/', include('hitcount.urls', namespace='hitcount'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns.append(path('admin/', admin.site.urls))
else:
    urlpatterns.append(path(str(os.getenv("ADMIN_LINK")), admin.site.urls))
