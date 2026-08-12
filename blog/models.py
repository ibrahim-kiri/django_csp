from django.db import models
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.CharField(max_length=100, default="Ibrahim")
    body = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Stores raw body text without sanitisation - intentional for the demo.
    The post_detail template renders comment.body through |safe so we can demonstrate a live XSS attack in Phase 0 and watch CSP block it in Phase 2+.
    """
    post  = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author_name = models.CharField(max_length=100)
    body = models.TextField() # raw - No sanitisation
    created_at = models.DateTimeField(default=timezone.now)
    approved = models.BooleanField(default=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.author_name} on '{self.post.title}'"
