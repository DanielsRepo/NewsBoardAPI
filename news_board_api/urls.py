from django.urls import path, include

from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    PostViewSet,
    CommentViewSet,
    UserViewSet,
    PostsByUserIdApiView,
    PostsByUserNameApiView,
    CommentsByUserIdApiView,
    CommentsByUserNameApiView,
    UpvotePostApiView,
)


router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"posts", PostViewSet, "posts")
router.register(r"comments", CommentViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("login/", obtain_auth_token),
    path("users/<int:pk>/posts/", PostsByUserIdApiView.as_view()),
    path("users/<username>/posts/", PostsByUserNameApiView.as_view()),
    path("users/<int:pk>/comments/", CommentsByUserIdApiView.as_view()),
    path("users/<username>/comments/", CommentsByUserNameApiView.as_view()),
    path("upvote/<int:pk>/", UpvotePostApiView.as_view()),
]
