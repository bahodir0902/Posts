from django.db import models
from typing import override
from django.contrib.auth.models import User

# Create your models here.
class PublishedPosts(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PB, is_deleted=0)

class DraftPosts(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.DR)


class Post(models.Model):
    class Status(models.TextChoices):
        DR = 'draft', 'Draft'
        PB = 'published', 'Published'
    title = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts', null=True, blank=True)
    slug = models.SlugField(max_length=255)
    # author = models.ForeignKey(User)
    body = models.TextField(null=True, blank=True)
    published_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(default=Status.DR, choices=Status.choices, max_length=20)
    is_deleted = models.BooleanField(default=False)

    published_posts = PublishedPosts()
    draft_posts = DraftPosts()

