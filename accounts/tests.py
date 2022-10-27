from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class SignUpTest(TestCase):
    def test_signup_url(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)

    def test_signup_url_by_name(self):
        response = self.client.get(reverse('signup'))

    def test_signup_form(self):
        get_user_model().objects.create_user(
            email='my_email',
            username='my_name'
        )
        response = self.client.get(reverse('signup'))
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].email, 'my_email')
        self.assertEqual(get_user_model().objects.all()[0].username, 'my_name')

    def test_signup_template_used(self):
        response = self.client.get(reverse('signup'))
        self.assertTemplateUsed(response, 'registration/signup.html')




