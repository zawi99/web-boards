from django.contrib.auth.models import User
from django.forms import ModelForm
from django.test import TestCase
from django.urls import reverse, resolve

from ..models import Board, Post, Topic
from ..views import PostEditView


class PostEditTestCase(TestCase):
    """
    Base test case to the all 'post-edit' view tests
    """

    def setUp(self):
        self.board = Board.objects.create(name='Django',
                                          description='About django')
        self.username = 'john'
        self.password = '123'
        user = User.objects.create_user(username=self.username,
                                        password=self.password,
                                        email='john@gmail.com')
        self.topic = Topic.objects.create(subject='Django tests',
                                          starter=user,
                                          board=self.board)
        self.post = Post.objects.create(topic=self.topic,
                                        created_by=user,
                                        message='post-edit test view')
        self.url = reverse('post-edit', kwargs={
            'pk': self.board.pk,
            'topic_pk': self.topic.pk,
            'post_pk': self.post.pk
        })


class LoginRequiredPostEditViewTests(PostEditTestCase):
    def test_redirection(self):
        """
        Test if only logged in user can edit the posts
        """
        login = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, f'{login}?next={self.url}')


class UnauthorizedPostEditViewTests(PostEditTestCase):
    def setUp(self):
        """
        Create a new user different from the one who posted
        """
        super().setUp()
        username = 'mark'
        password = '123'
        User.objects.create_user(username=username,
                                 email='mark@gmail.com',
                                 password=password)
        self.client.login(username=username, password=password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        """
        A topic should be edited only by the owner.
        Unauthorized users should get a 404 response (Page Not Found)
        """
        self.assertEquals(self.response.status_code, 404)


class PostEditViewTests(PostEditTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/boards/1/topic/1/post/1/edit/')
        self.assertEquals(view.func.view_class, PostEditView)

    def test_csrf_token(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)

    def test_form_inputs(self):
        """The form should contains two inputs: csrf and message textarea"""
        self.assertContains(self.response, '<input', 1)
        self.assertContains(self.response, '<textarea', 1)


class SuccessfulPostEditViewTests(PostEditTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)

        data = {
            'message': "Test message"
        }
        self.response = self.client.post(self.url, data)

    def test_redirection(self):
        """A valid submission should redirect the user"""
        topic_posts_url = reverse('topic-posts', kwargs={
            'pk': self.board.pk,
            'topic_pk': self.topic.pk
        })
        self.assertRedirects(self.response, topic_posts_url)

    def test_post_edited(self):
        self.post.refresh_from_db()
        self.assertEquals(self.post.message, "Test message")


class InvalidPostEditViewTests(PostEditTestCase):
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
