from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve

from ..forms import NewTopicForm
from ..models import (Board,
                      Topic,
                      Post)
from ..views import topic_new


class NewTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Piwko', description='O piwku.')
        User.objects.create_user(username='testuser',
                                 email='pies@o2.pl',
                                 password='123')
        self.client.login(username='testuser', password='123')

    def test_new_topic_view_success_status_code(self):
        url = reverse('topic-new', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        url = reverse('topic-new', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_topic_view_resolve_new_topic_view(self):
        view = resolve('/boards/1/new/')
        self.assertEquals(view.func, topic_new)

    def test_new_topic_view_contains_navigation_links(self):
        home_url = reverse('home')
        new_topic_url = reverse('topic-new', kwargs={'pk': 1})
        board_topics_url = reverse('topic-list', kwargs={'pk': 1})

        response = self.client.get(new_topic_url)
        self.assertContains(response, f'href="{board_topics_url}"')
        self.assertContains(response, f'href="{home_url}"')

    def test_csrf_token(self):
        url = reverse('topic-new', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_topic_valid_data_post(self):
        url = reverse('topic-new', kwargs={'pk': 1})
        data = {
            'subject': 'test subject',
            'message': 'some message to test'
        }
        self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_topic_invalid_data_post(self):
        """
        Invalid data should not be send by post
        The form with validation errors should be displayed
        """
        url = reverse('topic-new', kwargs={'pk': 1})
        data = {}
        response = self.client.post(url, data)
        form = response.context.get('form')
        self.assertTrue(form.errors)
        self.assertEquals(response.status_code, 200)

    def test_new_topic_invalid_data_post_empty_fields(self):
        """
        Invalid data should not be send by post
        The form with validation errors should be displayed
        """
        url = reverse('topic-new', kwargs={'pk': 1})
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())

    def test_contains_form(self):
        url = reverse('topic-new', kwargs={'pk': 1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)


class LoginRequiredNewTopicTests(TestCase):
    def setUp(self):
        board = Board.objects.create(name='Django', description='about django')
        self.url = reverse('topic-new', kwargs={'pk': board.pk})
        self.response = self.client.get(self.url)

    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, f'{login_url}?next={self.url}')
