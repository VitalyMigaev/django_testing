from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.test.client import Client
from django.urls import reverse

from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username="Автор")


@pytest.fixture
def reader(django_user_model):
    return django_user_model.objects.create(username='Читатель')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def reader_client(reader):
    client = Client()
    client.force_login(reader)
    return client


@pytest.fixture
def news(db):
    news = News.objects.create(
        title='Новость дня',
        text='День как день и машины туда-сюда...',
    )
    return news


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Неожиданная новость!',
    )
    return comment


@pytest.fixture
def news_data(db):
    today = datetime.today()
    News.objects.bulk_create(
        News(
            title=f'News {index}',
            text=f'Text of news: {index}.',
            date=today - timedelta(days=index),
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def news_with_comments(
        author,
        news
):
    today = datetime.today()
    comments = Comment.objects.bulk_create(
        Comment(
            news=news,
            author=author,
            text=f'Комментарий {index} к новости {news.id}!',
        )
        for index in range(5)
    )
    for index, comment in enumerate(comments):
        comment.created = today - timedelta(days=index)
        comment.save()


@pytest.fixture
def url_home():
    return reverse('news:home')


@pytest.fixture
def url_detail_news(news):
    news_detail_url = reverse('news:detail', args=[news.pk])
    return news_detail_url


@pytest.fixture
def url_edit_comment(comment):
    news_detail_url = reverse('news:edit', args=[comment.pk])
    return news_detail_url


@pytest.fixture
def url_delete_comment(comment):
    news_detail_url = reverse('news:delete', args=[comment.pk])
    return news_detail_url


@pytest.fixture
def url_users_login():
    url = reverse('users:login')
    return url


@pytest.fixture
def url_users_logout():
    url = reverse('users:logout')
    return url


@pytest.fixture
def url_users_signup():
    url = reverse('users:signup')
    return url
