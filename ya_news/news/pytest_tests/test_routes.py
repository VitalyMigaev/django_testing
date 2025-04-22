from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url',
    [
        pytest.lazy_fixture('url_home'),
        pytest.lazy_fixture('url_detail_news'),
        pytest.lazy_fixture('url_users_login'),
        pytest.lazy_fixture('url_users_logout'),
        pytest.lazy_fixture('url_users_signup')
    ]
)
def test_pages_availability_for_anonymous_users(client, url):
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'reverse_url, parametrized_client, status',
    [
        (
            pytest.lazy_fixture('url_edit_comment'),
            pytest.lazy_fixture('reader_client'),
            HTTPStatus.NOT_FOUND
        ),
        (
            pytest.lazy_fixture('url_edit_comment'),
            pytest.lazy_fixture('author_client'),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture('url_delete_comment'),
            pytest.lazy_fixture('reader_client'),
            HTTPStatus.NOT_FOUND
        ),
        (
            pytest.lazy_fixture('url_delete_comment'),
            pytest.lazy_fixture('author_client'),
            HTTPStatus.OK
        ),
    ]
)
def test_pages_availability_for_authorized_users(
        reverse_url,
        parametrized_client,
        comment,
        status,
):
    response = parametrized_client.get(reverse_url)
    assert response.status_code == status


@pytest.mark.parametrize(
    'name',
    [
        pytest.lazy_fixture('url_edit_comment'),
        pytest.lazy_fixture('url_delete_comment'),
    ]
)
def test_redirect_anonymous_user(
        client,
        name,
        url_users_login,
):
    expected_url = f'{url_users_login}?next={name}'
    response = client.get(name)
    assertRedirects(response, expected_url)
