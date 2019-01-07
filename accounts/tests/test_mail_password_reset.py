from django.contrib.auth.models import User
from django.core import mail
from django.shortcuts import reverse
from django.test import TestCase


class PasswordResetMailTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='john',
                                 email='john@gmail.com',
                                 password='qwerty123')
        data = {
            'email': 'john@gmail.com'
        }
        password_reset_url = reverse('password_reset')
        self.response = self.client.post(password_reset_url, data)
        self.email = mail.outbox[0]

    def test_email_subject(self):
        expected = '[Web Boards] Password reset'
        actual = self.email.subject
        self.assertEquals(expected, actual)

    def test_email_body(self):
        body = self.email.body
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_token_url = reverse('password_reset_confirm',
                                           kwargs={
                                               'token': token,
                                               'uidb64': uid,
                                           })
        self.assertIn(password_reset_token_url, body)
        self.assertIn('john', body)
        self.assertIn('john@gmail.com', body)

    def test_email_to(self):
        self.assertEquals(['john@gmail.com'], self.email.to)
