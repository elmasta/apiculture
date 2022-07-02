from django.contrib import admin
from blog.models import *

class CoursAdmin(admin.ModelAdmin):
    list_display = ("name", "description")

admin.site.register(Cours, CoursAdmin)
