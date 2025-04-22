from http import HTTPStatus

from django.urls import reverse

from notes.tests.test_fixtures import TestFixtures


class TestRoutes(TestFixtures):

    def test_pages_availability_for_anonymous_user(self):
        urls = [
            self.url_notes_home,
            self.url_users_login,
            self.url_users_logout,
            self.url_users_signup,
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_auth_user(self):
        urls = [
            self.url_notes_list,
            self.url_notes_add,
            self.url_notes_success,
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_different_users(self):
        urls = [
            self.url_notes_detail,
            self.url_notes_edit,
            self.url_notes_delete
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
                response = self.reader_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_redirects(self):
        client = self.client
        login_url = reverse('users:login')
        urls = [
            ('notes:detail', (self.note.slug,)),
            ('notes:edit', (self.note.slug,)),
            ('notes:delete', (self.note.slug,)),
            ('notes:add', None),
            ('notes:success', None),
            ('notes:list', None)
        ]
        for name, args in urls:
            url = reverse(name, args=args)
            expected_url = f'{login_url}?next={url}'
            response = client.get(url)
            self.assertRedirects(response, expected_url)
