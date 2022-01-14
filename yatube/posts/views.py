# posts/views.py

from django.shortcuts import render, get_object_or_404
from typing import Type

from .models import Post, Group


def index(request):
    template: str = 'posts/index.html'
    title: str = 'Последние обновления на сайте'
    description: str = 'Главная страница проекта Yatube'
    posts_count: str = 10
    posts: Type[Post] = Post.objects.all()[:posts_count]
    context: dict[str, str] = {
        'title': title,
        'description': description,
        'posts': posts
    }
    return render(
        request,
        template,
        context,
    )


def group_list(request, slug):
    template: str = 'posts/group_list.html'
    title: str = f'Записи сообщества {slug}'
    posts_count: str = 10
    group_name: Type[Group] = get_object_or_404(Group, slug=slug)
    posts: Type[Post] = group_name.posts.all()[:posts_count]
    description: str = group_name.description
    context: dict[str, str] = {
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
