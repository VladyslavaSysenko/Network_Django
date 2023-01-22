
from django.urls import path

from . import views

urlpatterns = [
    path("", views.start, name="start"),
    path("posts/<int:page>", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new_post, name="new_post"),
    path("follow/<str:username>", views.follow_info, name="follow_info"),
    path("user/<str:username>/<int:page>", views.user_page, name="user_page"),
    path("following/<int:page>", views.following_posts, name="following_posts"),
    path("like/change/<str:post_id>", views.like, name="like"),
    path("like/info/<str:post_id>", views.like_info, name="like_info"),
    path("edit/<str:post_id>", views.edit, name="edit"),
    path("terms/<int:page>", views.paginator, name="terms-by-page")
]
