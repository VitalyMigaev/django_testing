import pytest
from django.conf import settings
from django.urls import reverse

from news.forms import CommentForm

pytestmark = pytest.mark.django_db


def test_news_count(client, news_data, url_home):
    response = client.get(url_home)
    news_on_page_count = response.context['object_list'].count()
    assert news_on_page_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, news_data, url_home):
    response = client.get(url_home)
    all_dates = [news.date for news in response.context['object_list']]
    assert all_dates == sorted(all_dates, reverse=True)


def test_comments_order(
        client, news_with_comments, url_detail_news,
    ):
    response = client.get(url_detail_news)
    comments = response.context['news'].comment_set.all()
    all_dates = [comment.created for comment in comments]
    assert all_dates == sorted(all_dates)


def test_comment_form_available_for_author(
        author_client,
        comment,
        url_detail_news,
):
    response = author_client.get(url_detail_news)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)


def test_comment_form_not_available_for_anonymous_user(
        client,
        comment,
        url_detail_news,
):
    response = client.get(url_detail_news,)
    assert 'form' not in response.context
