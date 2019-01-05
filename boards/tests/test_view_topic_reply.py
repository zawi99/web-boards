from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve

from ..forms import NewPostForm
from ..models import Board, Post, Topic
from ..views import topic_reply


class TopicReplyTestCase(TestCase):
    def setUp(self):
        """
        Base test case to the all 'topic-reply' view tests
        """
        self.board = Board.objects.create(name='Django',
                                          description='About django')
        self.username = 'john'
        self.password = '123'
        self.user = User.objects.create_user(username=self.username,
                                             password=self.password,
                                             email='john@gmail.com')
        self.topic = Topic.objects.create(subject='Django tests',
                                          starter=self.user,
                                          board=self.board)
        Post.objects.create(topic=self.topic,
                            created_by=self.user,
                            message='topic-reply test view')
        self.url = reverse('topic-reply', kwargs={
            'pk': self.board.pk,
            'topic_pk': self.topic.pk
        })


class LoginRequiredTopicReplyTestS(TopicReplyTestCase):
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, f'{login_url}?next={self.url}')


class TopicReplyTests(TopicReplyTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/boards/1/topic/1/reply/')
        self.assertEquals(view.func, topic_reply)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, NewPostForm)

    def test_form_inputs(self):
        """The form should contains 2 input: message and csrf token"""
        self.assertContains(self.response, '<input', 1)
        self.assertContains(self.response, '<textarea', 1)


class SuccessfulTopicReplyTests(TopicReplyTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)

        data = {
            'message': 'hello world!'
        }
        self.response = self.client.post(self.url, data)

    def test_redirection(self):
        """A valid submission should redirect the user"""
        url = reverse('topic-posts',
                      kwargs={'pk': self.board.pk,
                              'topic_pk': self.topic.pk})
        topic_posts_url = '{url}?page=1#2'.format(url=url)
        self.assertRedirects(self.response, topic_posts_url)

    def test_reply_created(self):
        """
        The total post count should be 2
        The one created in the 'TopicReplyTestCase' setUp
        and another created by the post data in this class
        """
        self.assertEquals(Post.objects.count(), 2)


class InvalidTopicReplyTests(TopicReplyTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        data = {}
        self.response = self.client.post(self.url, data)

    def test_status_code(self):
        """
        An invalid form submission should display the same page
        with validation errors
        """
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
