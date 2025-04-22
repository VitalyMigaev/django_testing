import pytest

from django.conf import settings
from django.urls import reverse

from news.forms import CommentForm

pytestmark = pytest.mark.django_db


def test_news_count(client, news_data, url_home):
    response = client.get(url_home)
    news_on_page = response.context['object_list']
    assert len(news_on_page) == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, news_data, url_home):
    response = client.get(url_home)
    news_list = response.context['object_list']
    all_dates = [news.date for news in news_list]
    assert all_dates == sorted(all_dates, reverse=True)


def test_comments_order(client, news_with_comments):
    news_detail_url = reverse('news:detail', args=[news_with_comments.pk])
    response = client.get(news_detail_url)
    comments = response.context['object'].comment_set.all()
    all_dates = [comment.created for comment in comments]
    sorted_dates = sorted(all_dates)
    assert all_dates == sorted_dates


def test_comment_form_available_for_author(
        author_client,
        comment,
        url_detail_comment
):
    response = author_client.get(url_detail_comment)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)


def test_comment_form_not_available_for_anonymous_user(
        client,
        comment,
        url_detail_comment,
):
    response = client.get(url_detail_comment)
    assert 'form' not in response.context
