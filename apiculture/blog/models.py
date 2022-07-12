from django.db import models
from django.contrib.auth.models import User


class Cours(models.Model):

    def __str__(self):
        return f'{self.name}'

    name = models.CharField(max_length=100, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    teatching = models.TextField(null=False)
    description = models.TextField(blank=True, null=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Event(models.Model):

    def __str__(self):
        return f'{self.name}'

    name = models.CharField(max_length=100, null=False)
    description = models.TextField(blank=True, null=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Introduction(models.Model):

    description = models.TextField(null=False)

class Description(models.Model):

    description = models.TextField(null=False)
