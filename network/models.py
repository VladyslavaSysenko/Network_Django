from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")
    text = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="like")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="like")

class Following(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

