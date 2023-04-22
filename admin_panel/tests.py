import random

from rest_framework.test import APITestCase
from comments.tests import get_test_user, create_test_book
from accounts.models import User
from quiz.tests import create_test_user

from read_book.models import Book


class RatingTest(APITestCase):
    def test_create_and_update_rate(self):
        (user_token, user_id) = get_test_user()
        for i in range(25):
            create_test_user()
        super_user = User.objects.get(id=user_id)
        super_user.is_superuser = True
        super_user.is_staff = True
        super_user.save()

        response = self.client.get(
            '/admin-panel/user/',
            HTTP_AUTHORIZATION=f'Token {user_token[0].key}',
            format='json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 20)

        response = self.client.get(
            '/admin-panel/user/?page=2',
            HTTP_AUTHORIZATION=f'Token {user_token[0].key}',
            format='json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 5)
