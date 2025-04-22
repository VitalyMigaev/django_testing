from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects


pytestmark = pytest.mark.django_db


def test_home_availability_for_anonymous_user(
        client,
        url_home,
):
    response = client.get(url_home)
    assert response.status_code == HTTPStatus.OK


def test_news_detail_availability_for_anonymous_user(
        client,
        url_detail_news,
):
    response = client.get(url_detail_news)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name',
    ('users:login', 'users:logout', 'users:signup')
)
def test_auth_pages_availability_for_anonymous_user(
        client,
        name,
):
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'reverse_url, parametrized_client, status',
    [
        (
            'news:edit',
            pytest.lazy_fixture('reader_client'),
            HTTPStatus.NOT_FOUND
        ),
        (
            'news:edit',
            pytest.lazy_fixture('author_client'),
            HTTPStatus.OK
        ),
        (
            'news:delete',
            pytest.lazy_fixture('reader_client'),
            HTTPStatus.NOT_FOUND
        ),
        (
            'news:delete',
            pytest.lazy_fixture('author_client'),
            HTTPStatus.OK
        ),
    ]
)
def test_pages_availability_for_different_users(
        parametrized_client,
        reverse_url,
        comment,
        status,
):
    url = reverse(reverse_url, args=(comment.id,))
    response = parametrized_client.get(url)
    assert response.status_code == status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, comment_object',
    (
        ('news:edit', pytest.lazy_fixture('comment')),
        ('news:delete', pytest.lazy_fixture('comment')),
    )
)
def test_redirect_anonymous_user(
        client,
        name,
        comment_object,
):
    login_url = reverse('users:login')
    url = reverse(name, args=(comment_object.id,))
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
