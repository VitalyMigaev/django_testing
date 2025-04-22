from http import HTTPStatus

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from notes.tests.test_fixtures import TestFixtures


class TestCreateNote(TestFixtures):

    def test_anonymous_user_cant_create_note(self):
        notes_count_before_test = Note.objects.count()
        response = self.client.post(self.url_notes_add, data=self.form_data)
        expected_url = f'{self.url_users_login}?next={self.url_notes_add}'
        self.assertRedirects(response, expected_url)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, notes_count_before_test)

    def user_can_create_note(self):
        Note.objects.all().delete()
        response = self.author_client.post(
            self.url_notes_add,
            data=self.form_data
        )
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)
        self.assertRedirects(response, f'{self.url_notes_add}')
        note = Note.objects.get()
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.author, self.author)


class TestNoteEditDelete(TestFixtures):

    def test_author_can_delete_note(self):
        notes_count_before_test = Note.objects.count()
        response = self.author_client.delete(self.url_notes_delete)
        self.assertRedirects(response, self.url_notes_success)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, notes_count_before_test - 1)

    def test_user_cant_delete_comment_of_other_author(self):
        notes_count_before_test = Note.objects.count()
        response = self.reader_client.delete(self.url_notes_delete)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, notes_count_before_test)

    def test_author_can_edit_comment(self):
        original_title = self.note.title
        original_text = self.note.text
        response = self.author_client.post(
            self.url_notes_edit,
            data=self.form_new_data
        )
        self.assertRedirects(response, self.url_notes_success)
        edited_note = Note.objects.get(id=self.note.id)
        self.assertNotEqual(edited_note.title, original_title)
        self.assertNotEqual(edited_note.text, original_text)
        self.assertEqual(edited_note.title, self.form_new_data['title'])
        self.assertEqual(edited_note.text, self.form_new_data['text'])
        self.assertEqual(edited_note.author, self.author)

    def test_user_cant_edit_comment_of_another_user(self):
        original_title = self.note.title
        original_text = self.note.text
        response = self.reader_client.post(
            self.url_notes_edit,
            data=self.form_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        edited_note = Note.objects.get(id=self.note.id)
        self.assertEqual(edited_note.title, original_title)
        self.assertEqual(edited_note.text, original_text)
        self.assertEqual(edited_note.author, self.note.author)


class TestNoteSlug(TestFixtures):

    def test_not_unique_slug(self):
        notes_count_before_test = Note.objects.count()
        self.form_data['slug'] = self.note.slug
        response = self.author_client.post(
            self.url_notes_add,
            data=self.form_data
        )
        self.assertEqual(Note.objects.count(), notes_count_before_test)
        self.assertFormError(
            response,
            'form',
            'slug',
            self.note.slug + WARNING
        )

    def test_empty_slug(self):
        Note.objects.all().delete()
        if 'slug' in self.form_data:
            self.form_data.pop('slug')
        response = self.author_client.post(
            self.url_notes_add,
            data=self.form_data
        )
        self.assertEqual(Note.objects.count(), 1)
        self.assertRedirects(response, self.url_notes_success)
        new_note = Note.objects.get()
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.slug, expected_slug)
