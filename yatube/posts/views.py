from typing import Union

from django.shortcuts import render, get_object_or_404
from django.db.models.query import QuerySet
from django.http import HttpRequest, Http404, HttpResponse

from .models import Post, Group

POSTS_COUNT: int = 10


def index(request: HttpRequest) -> HttpResponse:
    """Функция вызова главной страницы."""
    template: str = 'posts/index.html'
    title: str = 'Последние обновления на сайте'
    page: str = 'index'
    description: str = 'Главная страница проекта Yatube'
    posts: QuerySet = Post.objects.all()[:POSTS_COUNT]
    context: dict[str, Union[str, QuerySet]] = {
        'title': title,
        'description': description,
        'posts': posts,
        'page': page
    }
    return render(
        request,
        template,
        context,
    )


def group_list(request: HttpRequest, slug: str) -> HttpResponse:
    """Функция вызова страницы группы."""
    group_name: Union[Group, Http404] = get_object_or_404(
        Group,
        slug=slug
    )
    template: str = 'posts/group_list.html'
    title: str = f'Записи сообщества {group_name}'
    posts: QuerySet = group_name.posts.all()[:POSTS_COUNT]
    description: str = group_name.description
    context: dict[str, Union[str, QuerySet, Group]] = {
        'title': title,
        'description': description,
        'group_name': group_name,
        'posts': posts,
    }
    return render(
        request,
        template,
        context
    )
