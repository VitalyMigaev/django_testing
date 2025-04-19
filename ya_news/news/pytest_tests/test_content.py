from django.conf import settings
from django.urls import reverse

from news.forms import CommentForm


def test_news_count(client, news_data):
    home_url = reverse('news:home')
    response = client.get(home_url)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, news_data):
    home_url = reverse('news:home')
    response = client.get(home_url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


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

):
    news_detail_url = reverse('news:detail', args=[comment.pk])
    response = author_client.get(news_detail_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)


def test_comment_form_not_available_for_anonymous_user(
        client,
        comment,

):
    news_detail_url = reverse('news:detail', args=[comment.pk])
    response = client.get(news_detail_url)
    assert 'form' not in response.context
