import pytest

from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


pytestmark = pytest.mark.django_db

FORM_DATA = {'text': 'Новый комментарий', }


def test_user_can_create_comment(
        author_client,
        news,
        author,
        url_detail_news,
):
    Comment.objects.all().delete()
    response = author_client.post(url_detail_news, data=FORM_DATA)
    assertRedirects(response,
                   reverse(
                        'news:detail',
                        kwargs={'pk': news.pk}
                    ) + '#comments'
                    )
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
    assert new_comment.news.title == news.title
    assert new_comment.author == author
    assert new_comment.text == FORM_DATA['text']


def test_anonymous_user_cant_create_comment(
        client,
        url_detail_news,
):
    comments_count = Comment.objects.count()
    response = client.post(url_detail_news, data=FORM_DATA)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url_detail_news}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == comments_count


def test_user_cant_use_bad_words_in_comments(
        author_client,
        url_detail_news,
):
    comments_count = Comment.objects.count()
    FORM_DATA['text'] = f'Text with {BAD_WORDS[0]} used.'
    response = author_client.post(url_detail_news, data=FORM_DATA)
    assert 'form' in response.context
    assertFormError(response, 'form', 'text', errors=WARNING)
    assert Comment.objects.count() == comments_count


def test_author_can_edit_own_comment(
        author_client,
        comment,
        news,
        url_edit_comment,
):
    response = author_client.post(url_edit_comment, data=FORM_DATA)
    assert response.status_code == HTTPStatus.OK
    comment_from_db = Comment.objects.get(id=comment.pk)
    assert comment_from_db.text == comment.text
    assert comment_from_db.news.title == news.title


def test_user_cant_edit_other_users_comment(
        reader_client,
        comment,
        url_edit_comment,
):
    response = reader_client.post(url_edit_comment, data=FORM_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=comment.pk)
    assert comment_from_db.news == comment.news
    assert comment_from_db.author == comment.author


def test_author_can_delete_own_comment(
        author_client,
        comment,
        url_delete_comment,
):
    comments_count = Comment.objects.count()
    response = author_client.post(url_delete_comment)
    assertRedirects(response,
                    reverse(
                        'news:detail',
                        kwargs={'pk': comment.pk}
                    ) + '#comments'
                    )
    assert Comment.objects.count() == comments_count - 1


def test_user_cant_delete_other_users_comment(
        reader_client, comment, url_delete_comment,
    ):
    comments_count = Comment.objects.count()
    response = reader_client.post(url_delete_comment)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == comments_count
