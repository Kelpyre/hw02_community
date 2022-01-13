# posts/views.py

from django.shortcuts import render, get_object_or_404
# Импортируем модели, чтобы обратиться к ним
from .models import Post, Group


def index(request):
    template = 'posts/index.html'
    title = 'main'
    description = 'Главная страница проекта Yatube'
    # В переменную posts будет сохранена выборка из 10 объектов модели Post,
    # отсортированных по полю pub_date по убыванию
    # (от больших значений к меньшим)
    posts = Post.objects.order_by('-pub_date')[:10]
    context = {
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
    template = 'posts/group_list.html'
    title = slug
    description = f'Посты группы {slug} проекта Yatube'
    group_name = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group_name).order_by('-pub_date')[:10]
    context = {
        'title': title,
        'description': description,
        'group_name': group_name,
        'posts': posts
    }
    return render(request, template, context)
