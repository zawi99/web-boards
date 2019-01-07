from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve

from ..views import UserAccountView


class UserAccountTestCase(TestCase):
    def setUp(self):
        self.url = reverse('account-detail')


class LoginRequiredUserAccountTests(UserAccountTestCase):
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, f'{login_url}?next={self.url}')


class UserAccountTests(UserAccountTestCase):
    def setUp(self):
        super().setUp()
        username = 'john'
        password = '123'
        User.objects.create_user(username=username,
                                 password=password)
        self.client.login(username=username, password=password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/account/')
        self.assertEquals(view.func.view_class, UserAccountView)
