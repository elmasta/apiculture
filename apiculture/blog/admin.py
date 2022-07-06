from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from blog.models import *

# class CoursAdmin(admin.ModelAdmin):
#     list_display = ("name", "description")

class CoursAdmin(SummernoteModelAdmin):
    summernote_fields = ('teatching')
    list_display = ("name", "description")

admin.site.register(Cours, CoursAdmin)