from notes.forms import NoteForm
from notes.tests.test_fixtures import TestFixtures


class TestNotesList(TestFixtures):

    def test_pages_contain_form(self):
        urls = (
            (self.url_notes_add),
            (self.url_notes_edit),
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)

    def test_notes_list_does_not_contain_other_users_notes(self):
        response = self.author_client.get(self.url_notes_list)
        self.assertIn(self.note, response.context['object_list'])
        self.assertNotIn(self.note_of_reader, response.context['object_list'])
