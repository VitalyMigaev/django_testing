from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Leo Tolstoy')
        cls.notes = Note.objects.create(
            title='Заметка 1',
            text='Текст заметки 1',
            author=cls.author,
        )
        cls.reader = User.objects.create(username='Just reader')

    def test_pages_availability_for_anonymous_user(self):
        client = self.client
        urls = ['notes:home', 'users:login', 'users:logout', 'users:signup']
        for name in urls:
            url = reverse(name)
            response = client.get(url)
            self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_auth_user(self):
        self.client.force_login(self.author)
        urls = ['notes:list', 'notes:add', 'notes:success']
        for name in urls:
            url = reverse(name)
            response = self.client.get(url)
            self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_different_users(self):
        urls = ['notes:detail', 'notes:edit', 'notes:delete']
        for name in urls:
            url = reverse(name, args=(self.notes.slug,))
            self.client.force_login(self.author)
            response = self.client.get(url)
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.client.force_login(self.reader)
            response = self.client.get(url)
            self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_redirects(self):
        client = self.client
        login_url = reverse('users:login')
        urls = [
            ('notes:detail', (self.notes.slug,)),
            ('notes:edit', (self.notes.slug,)),
            ('notes:delete', (self.notes.slug,)),
            ('notes:add', None),
            ('notes:success', None),
            ('notes:list', None)
        ]
        for name, args in urls:
            url = reverse(name, args=args)
            expected_url = f'{login_url}?next={url}'
            response = client.get(url)
            self.assertRedirects(response, expected_url)
