from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.test import TestCase
from django.urls import resolve, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class PasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_csrf_token(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_view_function(self):
        view = resolve('/password/reset/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetView)

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordResetForm)

    def test_form_inputs(self):
        """
        The response should contain only two inputs: email and csrf
        """
        self.assertContains(self.response, '<input', 2)
        self.assertContains(self.response, 'type="email"', 1)


class SuccessfulPasswordResetTests(TestCase):
    def setUp(self):
        email = 'john@o2.pl'
        User.objects.create_user(username='john', email=email,
                                 password='qwerty1234')
        url = reverse('password_reset')
        data = {
            'email': email,
        }
        self.response = self.client.post(url, data)

    def test_redirection(self):
        """
        A valid form submission should redirect to the 'password_reset_done' view.
        """
        password_reset_done_url = reverse('password_reset_done')
        self.assertRedirects(self.response, password_reset_done_url)

    def test_send_password_reset_email(self):
        self.assertEquals(1, len(mail.outbox))


class InvalidPasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        email = 'doesnotexist@o2.pl'
        data = {
            'email': email,
        }
        self.response = self.client.post(url, data)

    def test_redirection(self):
        """
        If the email address provided does not exist in the system, the user is inactive,
        or has an unusable password, the user will still be redirected to this view but
        no email will be sent.
        """
        password_reset_done_url = reverse('password_reset_done')
        self.assertRedirects(self.response, password_reset_done_url)

    def test_no_email_reset_sent(self):
        self.assertEquals(0, len(mail.outbox))


class PasswordResetDoneTests(TestCase):
    def setUp(self):
        url = reverse('password_reset_done')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/password/reset/done/')
        self.assertEquals(view.func.view_class,
                          auth_views.PasswordResetDoneView)


class ValidPasswordResetConfirmTests(TestCase):
    def setUp(self):
        email = 'john@gmail.com'
        user = User.objects.create_user(username='john', email=email,
                                        password='qwerty1234')

        '''
        create a valid password reset token
        based on how django creates the token internally:
        https://github.com/django/django/blob/stable/1.11.x/django/contrib/auth/forms.py#L280
        '''
        self.uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        self.token = default_token_generator.make_token(user)

        url = reverse('password_reset_confirm', kwargs={
            'uidb64': self.uid,
            'token': self.token
        })
        self.response = self.client.get(url, follow=True)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve(f'/password/reset/{self.uid}/{self.token}/')
        self.assertEquals(view.func.view_class,
                          auth_views.PasswordResetConfirmView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SetPasswordForm)

    def test_form_inputs(self):
        """The form should contains 3 inputs: csrf and two password inputs"""
        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, 'type="password"', 2)


class InvalidPasswordResetConfirmTests(TestCase):
    def setUp(self):
        email = 'john@gmail.com'
        user = User.objects.create_user(username='john', email=email,
                                        password='qwerty1234')
        self.uid = urlsafe_base64_encode(force_bytes(user.pk))
        self.token = default_token_generator.make_token(user)

        '''
        invalidate the token by changing the password
        '''
        user.set_password('abcdef1234')
        user.save()

        url = reverse('password_reset_confirm', kwargs={
            'uidb64': self.uid,
            'token': self.token
        })
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_html(self):
        password_reset_url = reverse('password_reset')
        self.assertContains(self.response, 'invalid password reset link')
        self.assertContains(self.response, f'href="{password_reset_url}"')


class PasswordResetCompleteTests(TestCase):
    def setUp(self):
        url = reverse('password_reset_complete')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/password/reset/complete/')
        self.assertEquals(view.func.view_class,
                          auth_views.PasswordResetCompleteView)
