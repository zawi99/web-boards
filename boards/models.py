from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse
from django.utils.text import Truncator


class Board(models.Model):
    name = models.CharField(max_length=30,
                            unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by(
            '-created_by').first()

    def get_post_count(self):
        return Post.objects.filter(topic__board=self).count()


class Topic(models.Model):
    board = models.ForeignKey(Board, related_name='topics')
    starter = models.ForeignKey(User, related_name='topics')
    subject = models.CharField(max_length=255)
    views = models.PositiveIntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, related_name='posts',
                              on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+')

    created_by = models.ForeignKey(User, related_name='posts')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)
