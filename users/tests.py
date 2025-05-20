from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class UserTests(TestCase):
    def test_user_can_register(self):
        """Пользователь успешно регистрируется"""
        response = self.client.post(reverse('register'), {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'pass1234',
            'password2': 'pass1234',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='test@example.com').exists())

    def test_user_can_login(self):
        """Пользователь успешно входит"""
        User.objects.create_user(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='pass1234'
        )
        response = self.client.post(reverse('login'), {
            'email': 'test@example.com',
            'password': 'pass1234',
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('_auth_user_id', self.client.session)
