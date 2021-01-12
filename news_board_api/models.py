from django.db import models
from django.conf import settings
from django.utils import timezone


class PostManager(models.Manager):
    def created(self):
        return self.order_by("-creation_date")

    def by_user(self, user):
        return self.filter(author=user).order_by("-creation_date")


class Post(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField()
    creation_date = models.DateTimeField(default=timezone.now)
    upvotes_amount = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )

    objects = PostManager()


class CommentManager(models.Manager):
    def created(self):
        return self.order_by("-creation_date")

    def by_user(self, user):
        return self.filter(author=user).order_by("-creation_date")

    def by_post(self, post):
        return self.filter(post=post).order_by("-creation_date")


class Comment(models.Model):
    text = models.TextField()
    creation_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    post = models.ForeignKey("Post", on_delete=models.CASCADE, null=True)

    objects = CommentManager()
