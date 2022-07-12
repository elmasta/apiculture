from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from blog.models import *


class CoursAdmin(SummernoteModelAdmin):
    summernote_fields = ('teatching')
    list_display = ("name", "description")

class EventAdmin(SummernoteModelAdmin):
    summernote_fields = ('description')
    list_display = ("name", "description")

class IntroductionAdmin(SummernoteModelAdmin):
    summernote_fields = ('description')

class DescriptionAdmin(SummernoteModelAdmin):
    summernote_fields = ('description')

admin.site.register(Cours, CoursAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Introduction, IntroductionAdmin)
admin.site.register(Description, DescriptionAdmin)
