from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve

from ..models import Board, Post, Topic
from ..views import PostListView


class TopicPostsTests(TestCase):
    def setUp(self):
        board = Board.objects.create(name='Django',
                                     description='About Dango!')
        user = User.objects.create_user(username='john',
                                        email='john@gmail.com',
                                        password='qwerty1234')
        topic = Topic.objects.create(board=board,
                                     starter=user,
                                     subject='Django tests')
        post = Post.objects.create(
            message='Learning \'how to\' test in Django.',
            topic=topic,
            created_by=user,
        )
        self.url = reverse('topic-posts', kwargs={
            'pk': topic.board.pk,
            'topic_pk': topic.pk
        })
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/boards/1/topic/1/')
        self.assertEquals(view.func, PostListView)