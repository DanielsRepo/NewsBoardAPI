from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS

from .models import Post, Comment
from .serializers import PostSerializer, UserSerializer, CommentSerializer


class IsAuthenticatedOrCreate(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        return super(IsAuthenticatedOrCreate, self).has_permission(request, view)


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrCreate | ReadOnly]

    def update(self, request, *args, **kwargs):
        user = get_object_or_404(User.objects.all(), pk=self.kwargs["pk"])
        if request.user != user:
            raise PermissionDenied("You can't update someone else's account")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        admin = get_object_or_404(User.objects.all(), username="admin")
        if request.user != admin:
            raise PermissionDenied(
                "Only admin can delete someone else's account with his posts"
            )
        return super().destroy(request, *args, **kwargs)


class PostsByUserIdApiView(ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        if "pk" in self.kwargs:
            return Post.objects.by_user(self.kwargs["pk"])


class PostsByUserNameApiView(ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        if "username" in self.kwargs:
            return Post.objects.by_user(
                User.objects.get(username=self.kwargs["username"])
            )


class CommentsByUserIdApiView(ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        if "pk" in self.kwargs:
            return Comment.objects.by_user(self.kwargs["pk"])


class CommentsByUserNameApiView(ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        if "username" in self.kwargs:
            return Comment.objects.by_user(
                User.objects.get(username=self.kwargs["username"])
            )


class PostViewSet(ModelViewSet):
    queryset = Post.objects.created()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        post_saved = serializer.save()
        post_saved.author = self.request.user
        post_saved.link = reverse("posts-detail", kwargs={"pk": post_saved.pk})
        return super().perform_create(serializer)

    def update(self, request, *args, **kwargs):
        post = get_object_or_404(Post.objects.all(), pk=self.kwargs["pk"])
        if request.user != post.author:
            raise PermissionDenied("You can't update someone else's post")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        post = get_object_or_404(Post.objects.all(), pk=self.kwargs["pk"])
        if request.user != post.author:
            raise PermissionDenied("You can't delete someone else's post")
        return super().destroy(request, *args, **kwargs)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.created()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        comment_saved = serializer.save()
        comment_saved.author = self.request.user
        return super().perform_create(serializer)

    def update(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment.objects.all(), pk=self.kwargs["pk"])
        if request.user != comment.author:
            raise PermissionDenied("You can't update someone else's comment")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment.objects.all(), pk=self.kwargs["pk"])
        if request.user != comment.author:
            raise PermissionDenied("You can't delete someone else's comment")
        return super().destroy(request, *args, **kwargs)


class UpvotePostApiView(APIView):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post.objects.all(), pk=self.kwargs["pk"])
        post.upvotes_amount += 1
        post.save()
        return Response(
            data={"success": "Post is upvoted", "link": f"{post.link}"}, status=200
        )