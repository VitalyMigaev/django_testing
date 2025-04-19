from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


def test_user_can_create_comment(
        author_client,
        news,
        form_data,
        author,
):
    url = reverse('news:detail', kwargs={'pk': news.pk})
    response = author_client.post(url, data=form_data)
    assertRedirects(response,
                    reverse(
                        'news:detail',
                        kwargs={'pk': news.pk}
                    ) + '#comments'
                    )
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
    assert new_comment.author == author
    assert new_comment.text == form_data['text']


def test_anonymous_user_cant_create_comment(
        client,
        news,
        form_data,
):
    url = reverse('news:detail', kwargs={'pk': news.pk})
    response = client.post(url, data=form_data)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 0


def test_user_cant_use_bad_words_in_comments(
        author_client,
        news,
        form_data,
):
    url = reverse('news:detail', kwargs={'pk': news.pk})
    form_data['text'] = f'Text with {BAD_WORDS[0]} used.'
    response = author_client.post(url, data=form_data)
    assert 'form' in response.context
    assertFormError(response, 'form', 'text', errors=WARNING)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_edit_own_comment(
        author_client,
        form_data,
        news,
        author,
):
    url = reverse('news:detail', args=[news.pk])
    response = author_client.post(url, data=form_data)
    assertRedirects(response,
                    reverse(
                        'news:detail',
                        kwargs={'pk': news.pk}
                    ) + '#comments'
                    )
    news.refresh_from_db()
    comment = news.comment_set.first()
    assert comment.author == author
    assert comment.text == form_data['text']


def test_user_cant_edit_other_users_comment(
        reader_client,
        form_data,
        comment,
):
    url = reverse('news:edit', args=[comment.pk])
    response = reader_client.post(url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.first()
    assert comment_from_db.text == comment.text


def test_author_can_delete_own_comment(
        author_client,
        comment,
):
    url = reverse('news:delete', args=[comment.pk])
    response = author_client.post(url)
    assertRedirects(response,
                    reverse(
                        'news:detail',
                        kwargs={'pk': comment.pk}
                    ) + '#comments'
                    )
    assert Comment.objects.count() == 0


def test_user_cant_delete_other_users_comment(reader_client, comment):
    url = reverse('news:delete', args=[comment.pk])
    response = reader_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
