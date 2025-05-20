from django.db import models
from django.conf import settings


class Task(models.Model):
    """Задача, принадлежащая пользователю"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)

    def __str__(self):
        """Возвращает название задачи"""
        return self.title
