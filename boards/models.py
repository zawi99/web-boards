import markdown
import math

from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.text import Truncator


class Board(models.Model):
    name = models.CharField(max_length=30,
                            unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by(
            '-created_at').first()

    def get_post_count(self):
        return Post.objects.filter(topic__board=self).count()


class Topic(models.Model):
    board = models.ForeignKey(Board, related_name='topics')
    starter = models.ForeignKey(User, related_name='topics')
    subject = models.CharField(max_length=255)
    views = models.PositiveIntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    # last_update is overwritten in topic_reply view
    last_update = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

    def get_page_count(self):
        paginate_by = 20
        posts = self.posts.count()
        pages = posts / paginate_by
        return math.ceil(pages)

    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 6

    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 1)

    def get_last_ten_posts(self):
        return self.posts.order_by('-created_at')[:10]


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

    def get_message_as_markdown(self):
        markdown_message = markdown.markdown(self.message)
        return mark_safe(markdown_message)
