from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.test.client import Client

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
    news_items = News.objects.bulk_create(
        News(
            title=f'News {index}',
            text=f'Text of news: {index}.',
            date=today - timedelta(days=index),
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )
    return news_items


@pytest.fixture
def news_with_comments(
        author,
        news
):
    today = datetime.today()
    Comment.objects.bulk_create(
        Comment(
            news=news,
            author=author,
            text=f'Комментарий {index} к новости {news.id}!',
            created=today - timedelta(days=index),
        )
        for index in range(5)
    )
    return news


@pytest.fixture
def form_data(author):
    return {
        'text': 'Новый комментарий',
        'author': author,
    }
