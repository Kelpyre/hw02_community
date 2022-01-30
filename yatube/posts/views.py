from typing import Union

from django.shortcuts import redirect, render, get_object_or_404
from django.db.models.query import QuerySet
from django.http import HttpRequest, Http404, HttpResponse
from django.core.paginator import Paginator, Page
from django.utils.text import Truncator
from django.contrib.auth.decorators import login_required

from .models import Post, Group, User
from .forms import PostForm


def index(request: HttpRequest) -> HttpResponse:
    """Функция вызова главной страницы."""
    template: str = 'posts/index.html'
    title: str = 'Последние обновления на сайте'
    description: str = 'Главная страница проекта Yatube'
    posts: QuerySet = Post.objects.all()
    paginator: Paginator = Paginator(posts, 10)
    page_number: Union[str, None] = request.GET.get('page')
    page_obj: Page = paginator.get_page(page_number)
    context: dict[str, Union[str, Page]] = {
        'title': title,
        'description': description,
        'page_obj': page_obj,
    }
    return render(
        request,
        template,
        context,
    )


@login_required
def group_list(request: HttpRequest, slug: str) -> HttpResponse:
    """Функция вызова страницы группы."""
    group_name: Union[Group, Http404] = get_object_or_404(
        Group,
        slug=slug
    )
    template: str = 'posts/group_list.html'
    title: str = f'Записи сообщества {group_name}'
    posts: QuerySet = group_name.posts.all()
    description: str = group_name.description
    paginator: Paginator = Paginator(posts, 10)
    page_number: Union[str, None] = request.GET.get('page')
    page_obj: Page = paginator.get_page(page_number)
    context: dict[str, Union[str, Page, Group]] = {
        'title': title,
        'description': description,
        'group_name': group_name,
        'page_obj': page_obj,
    }
    return render(
        request,
        template,
        context
    )


@login_required
def profile(request, username):
    # Здесь код запроса к модели и создание словаря контекста
    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    posts_count = posts.count()
    title = f'Профайл пользователя {username}'
    paginator: Paginator = Paginator(posts, 10)
    page_number: Union[str, None] = request.GET.get('page')
    page_obj: Page = paginator.get_page(page_number)
    context = {
        'title': title,
        'page_obj': page_obj,
        'posts_count': posts_count,
    }
    return render(request, template, context)


@login_required
def post_detail(request, post_id):
    WORD_COUNT = 30
    # Здесь код запроса к модели и создание словаря контекста
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, pk=post_id)
    posts_count = Post.objects.select_related('author').count()
    first_30 = Truncator(post.text).words(WORD_COUNT)
    title = f'Пост {first_30}'
    context = {
        'title': title,
        'post': post,
        'posts_count': posts_count,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    template = 'posts/create_post.html'
    title = 'Новый пост'
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            added_post = form.save(commit=False)
            added_post.author = request.user
            form.save(commit=True)
            author = request.user
            return redirect('posts:profile', author)
        else:
            return render(request, template, {
                'form': form,
                'title': title,
                }
            )

    form = PostForm()
    return render(request, template, {
        'form': form,
        'title': title,
        }
    )
