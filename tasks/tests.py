from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Task

User = get_user_model()


class TaskTests(TestCase):
    def setUp(self):
        """Создаёт пользователя и выполняет вход перед каждым тестом"""
        self.user = User.objects.create_user(
            email='user@example.com', first_name='First', last_name='Last', password='pass123'
        )
        self.client.login(email='user@example.com', password='pass123')

    def test_create_task(self):
        """Проверяет создание новой задачи"""
        response = self.client.post(reverse('task_list'), {'title': 'New Task'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title='New Task', user=self.user).exists())

    def test_toggle_task(self):
        """Проверяет переключение статуса задачи"""
        task = Task.objects.create(user=self.user, title='Task to toggle', completed=False)
        response = self.client.get(reverse('toggle_task', args=[task.id]))
        self.assertEqual(response.status_code, 302)
        task.refresh_from_db()
        self.assertTrue(task.completed)

    def test_delete_task(self):
        """Проверяет удаление задачи"""
        task = Task.objects.create(user=self.user, title='Task to delete')
        response = self.client.get(reverse('delete_task', args=[task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=task.id).exists())
