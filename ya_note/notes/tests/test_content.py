from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()


class TestNotesList(TestCase):
    NOTES_LIST_URL = reverse('notes:list')

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username="author")
        cls.reader = User.objects.create(username="reader")
        cls.note_of_author = Note.objects.create(
            title='Заметка автора',
            text='Текст заметки автора',
            author=cls.author,
        )
        cls.note_of_reader = Note.objects.create(
            title='Заметка читателя',
            text='Текст заметки читателя',
            author=cls.reader,
        )
        all_notes = []
        for index in range(settings.NOTES_COUNT_ON_HOME_PAGE + 1):
            notes = Note.objects.create(
                title=f'Заметка {index}',
                text='Просто текст заметки.',
                author=cls.author,
            )
            all_notes.append(notes)
            notes.save()

    def setUp(self):
        self.author_client = Client()
        self.author_client.force_login(self.author)
        self.reader_client = Client()
        self.reader_client.force_login(self.reader)

    def test_notes_list_count(self):
        response = self.author_client.get(self.NOTES_LIST_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        object_list = response.context['object_list']
        notes_count = object_list.count()
        self.assertEqual(notes_count, settings.NOTES_COUNT_ON_HOME_PAGE + 2)

    def test_pages_contain_form_add(self):
        url = reverse('notes:add')
        response = self.author_client.get(url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)

    def test_pages_contain_form_edit(self):
        url = reverse('notes:edit', args=[self.note_of_author.slug])
        response = self.author_client.get(url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)

    def test_notes_list_does_not_contain_other_users_notes(self):
        response = self.author_client.get(self.NOTES_LIST_URL)
        object_list = response.context['object_list']
        self.assertIn(self.note_of_author, object_list)
        self.assertNotIn(self.note_of_reader, object_list)
