from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()
POST_STATUS = (
    ('draft', 'Draft'),
    ('publish', "Publish")
)


class PostQuerySet(models.query.QuerySet):
    def draft(self):
        return self.filter(status='draft')

    def publish(self):
        return self.filter(status='publish')


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model)

    def draft(self):
        return self.get_queryset().draft()

    def publish(self):
        return self.get_queryset().publish()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    body = RichTextUploadingField(null=True)
    status = models.CharField(max_length=20, choices=POST_STATUS)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = PostManager()

    class Meta:
        default_related_name = 'posts'
        ordering = ('created',)

    def __str__(self):
        return f"{self.id}: {self.title}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.CharField(max_length=60)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        default_related_name = 'comments'
        ordering = ('created',)

    def __str__(self):
        return f"{self.id}: {self.author}"


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    session_key = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        default_related_name = 'likes'
        unique_together = (("post", "session_key"),)

