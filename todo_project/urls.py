from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect

from users.views import register_view, login_view, logout_view
from tasks.views import task_list, toggle_task_view, delete_task_view


urlpatterns = [
    path('admin/', admin.site.urls),

    # Главная перенаправляет на login
    path('', lambda request: redirect('login'), name='home'),

    # Аутентификация
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Задачи
    path('tasks/', task_list, name='task_list'),
    path('toggle/<int:task_id>/', toggle_task_view, name='toggle_task'),
    path('delete/<int:task_id>/', delete_task_view, name='delete_task'),
]
