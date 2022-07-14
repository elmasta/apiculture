from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from django.shortcuts import reverse


class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    ip = models.CharField(max_length=30)
    is_moderator = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)

    @property
    def num_posts(self):
        return Post.objects.filter(user=self).count()

    def __str__(self):
        try:
            return self.user.username
        except AttributeError:
            return "User Deleted"

class Banned_IP(models.Model):
    ip = models.CharField(max_length=30)

class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "categories"


    def __str__(self):
        return self.title
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def get_url(self):
        return reverse("posts", kwargs={
            "slug":self.slug
        })

    @property
    def num_posts(self):
        return Post.objects.filter(categories=self, approved=True).count()
    
    @property
    def last_post(self):
        return Post.objects.filter(categories=self).latest("date")


# création de topic
class Post(models.Model):
    title = models.CharField(max_length=400)
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    user = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )
    closed = models.BooleanField(default=False)
    state = models.CharField(max_length=40, default="zero")
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse("detail", kwargs={
            "slug":self.slug
        })
    
    @property
    def last_reply(self):
        return Reply.objects.filter(post=self).latest("date")


# réponse à un topic
class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:100]

    class Meta:
        verbose_name_plural = "replies"
   