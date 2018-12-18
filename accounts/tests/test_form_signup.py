from django.test import TestCase

from ..forms import SingUpForm


class SingUpFormTests(TestCase):
    def test_form_has_fields(self):
        form = SingUpForm()
        expected = ['username', 'email', 'password1', 'password2']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)
