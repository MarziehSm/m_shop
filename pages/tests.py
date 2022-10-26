from django.test import TestCase
from django.urls import reverse


class TestPages(TestCase):
    def test_home_page_view_url(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_view_url_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_name_page_on_home_page_view(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Home')

    def test_aboutus_page_view_url(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

    def test_aboutus_page_view_url_by_name(self):
        response = self.client.get(reverse('aboutus'))
        self.assertEqual(response.status_code, 200)

    def test_name_page_on_aboutus_page_view(self):
        response = self.client.get(reverse('aboutus'))
        self.assertContains(response, 'jh')
