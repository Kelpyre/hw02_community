# posts/urls.py

from django.urls import path
# Импорт для связи с view-функциями
from . import views

# Запись для include() в основной urls.py
app_name = 'posts'

urlpatterns = [
    # Путь для главной страницы
    path(
        '',
        views.index,
        name='index'
    ),
    # Путь до страниц сообществ, через slug (регулярное выражение?)
    # Аналогично можно реализовать через re_path
    path(
        'group/<slug:slug>/',
        views.group_list,
        name='group_list'
    )
]
