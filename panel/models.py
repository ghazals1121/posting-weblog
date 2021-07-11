from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class MyUser(AbstractUser):
    email = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)


class Post(models.Model):
    post_id = models.CharField(max_length=15, unique=True)
    author = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.FileField(null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    users_liked = models.ManyToManyField(MyUser, related_name='liked_post', null=True, blank=True)
    users_disliked = models.ManyToManyField(MyUser, related_name='disliked_post', null=True, blank=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    REQUIRED_FIELDS = ['post_id', 'author']


class Comment(models.Model):
    comment_id = models.CharField(max_length=15, unique=True)
    author = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    users_liked = models.ManyToManyField(MyUser, related_name='liked_comment', null=True, blank=True)
    users_disliked = models.ManyToManyField(MyUser, related_name='disliked_comment', null=True, blank=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    REQUIRED_FIELDS = ['post', 'author', 'text']


class Reply(models.Model):
    reply_id = models.CharField(max_length=15, unique=True)
    author = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    text = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = ['comment', 'author', 'text']
