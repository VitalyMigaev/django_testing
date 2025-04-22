from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestFixtures(TestCase):
    NOTE_TITLE = 'Заметка про погоду'
    NOTE_TEXT = 'Текст заметки про погоду'
    NOTE_SLUG = 'novaya-zametka'
    NEW_NOTE_TITLE = 'Заметка2 про погоду'
    NEW_NOTE_TEXT = 'Текст 2 заметки про погоду'
    NEW_NOTE_SLUG = 'novaya2-zametka'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Leo Tolstoy')
        cls.client = Client()
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.note = Note.objects.create(
            title=cls.NOTE_TITLE,
            text=cls.NOTE_TEXT,
            slug=cls.NOTE_SLUG,
            author=cls.author,
        )
        cls.reader = User.objects.create(username='Just reader')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.note_of_reader = Note.objects.create(
            title='Заметка читателя',
            text='Текст заметки читателя',
            author=cls.reader,
        )
        cls.form_data = {
            'title': cls.NOTE_TITLE,
            'text': cls.NOTE_TEXT,
            'slug': cls.NOTE_SLUG,
        }
        cls.form_new_data = {
            'title': cls.NEW_NOTE_TITLE,
            'text': cls.NEW_NOTE_TEXT
        }
        cls.url_notes_home = reverse('notes:home')
        cls.url_notes_list = reverse('notes:list')
        cls.url_notes_add = reverse('notes:add')
        cls.url_notes_detail = reverse(
            'notes:detail',
            args=[cls.note.slug]
        )
        cls.url_notes_edit = reverse(
            'notes:edit',
            args=[cls.note.slug]
        )
        cls.url_notes_delete = reverse(
            'notes:delete',
            args=[cls.note.slug]
        )
        cls.url_notes_success = reverse('notes:success')
        cls.url_users_login = reverse('users:login')
        cls.url_users_logout = reverse('users:logout')
        cls.url_users_signup = reverse('users:signup')
