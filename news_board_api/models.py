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
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    objects = PostManager()

    def upvote(self):
        self.upvotes_amount += 1
        self.save()

    @classmethod
    def reset_upvotes(Post):
        print("Resetting post upvotes count...")
        Post.objects.all().update(upvotes_amount=0)
        print("Post upvotes count has been reseted")


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
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    objects = CommentManager()
