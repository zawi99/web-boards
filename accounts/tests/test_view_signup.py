from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import TestCase
from django.urls import resolve

from ..forms import SingUpForm
from ..views import signup


class SingupTests(TestCase):
    def setUp(self):
        self.url = reverse('signup')
        self.response = self.client.get(self.url)

    def test_singup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_singup_url_resolves_singup_view(self):
        view = resolve('/signup/')
        self.assertEqual(view.func, signup)

    def test_csrf_token(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SingUpForm)

    def test_form_inputs(self):
        """
        The SingUpForm should contain 5 inputs: csrf, username, email,
        password1, password2
        """
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="password"', 2)
        self.assertContains(self.response, 'type="email"', 1)


class SuccessfulSingUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        data = {
            'username': 'testuser',
            'email': 'testemail@gmail.com',
            'password1': 'qwerty1234',
            'password2': 'qwerty1234',
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('home')

    def test_redirection(self):
        """
        After successful sign up the user should be redirected to home page
        """
        self.assertRedirects(self.response, self.home_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        """
        Create new request to some page.
        The response should have 'user' in its context, after successful sign up.
        """
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidSingUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        data = {}
        self.response = self.client.post(url, data)

    def test_sing_up_status_code(self):
        """
        An invalid form submission should redirect to the same page
        """
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_do_not_create_user(self):
        self.assertFalse(User.objects.exists())
