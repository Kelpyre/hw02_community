from typing import Union
from django.shortcuts import render, get_object_or_404
from django.db.models.query import QuerySet
from django.http import HttpRequest, Http404, HttpResponse

from .models import Post, Group

posts_count: int = 10


def index(request: HttpRequest) -> HttpResponse:
    template: str = 'posts/index.html'
    title: str = 'Последние обновления на сайте'
    description: str = 'Главная страница проекта Yatube'
    posts: QuerySet[Post] = Post.objects.all()[:posts_count]
    context: dict[str, Union[str, QuerySet]] = {
        'title': title,
        'description': description,
        'posts': posts
    }
    return render(
        request,
        template,
        context,
    )


def group_list(request: HttpRequest, slug: str) -> HttpResponse:
    template: str = 'posts/group_list.html'
    title: str = f'Записи сообщества {slug}'
    group_name: Union[Group.title, Http404] = get_object_or_404(
        Group,
        slug=slug
    )
    posts: QuerySet[Post] = group_name.posts.all()[:posts_count]
    description: str = group_name.description
    context: dict[str, Union[str, QuerySet[Post], Group.title]] = {
        'title': title,
        'description': description,
        'group_name': group_name,
        'posts': posts
    }
    return render(
        request,
        template,
        context
    )
