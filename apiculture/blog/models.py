from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profil_picture = models.ImageField(upload_to=get_userpic_path, blank=True,
                                       null=True,
                                       validators=[validate_picture])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)