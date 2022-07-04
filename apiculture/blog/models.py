from django.db import models
from django.contrib.auth.models import User

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     profil_picture = models.ImageField(upload_to=get_userpic_path, blank=True,
#                                        null=True,
#                                        validators=[validate_picture])

class Cours(models.Model):

    def __str__(self):
        return f'{self.name}'

    name = models.CharField(max_length=100, null=False)
    teatching = models.TextField(null=False)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)