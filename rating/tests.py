import random

import requests
from django.test import TestCase
from rest_framework.test import APITestCase
from comments.tests import get_test_user, create_test_book
from accounts.models import User

# Create your tests here.
from read_book.models import Book


class RatingTest(APITestCase):
    def test_create_and_update_rate(self):
        (user_token, user_id) = get_test_user()
        book_id = create_test_book()
        user = User.objects.get(id=user_id)
        book = Book.objects.get(pk=book_id)
        rate = random.randint(1, 5)

        response = self.client.post(
            '/rate/',
            HTTP_AUTHORIZATION=f'Token {user_token[0].key}',
            data={
                "book": book.id,
                "rate": rate
            },
            format='json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['user'], user.id)
        self.assertEqual(response.json()['book'], book.id)
        self.assertEqual(response.json()['rate'], rate)

        new_rate = (rate - 1) % 5
        if new_rate == 0:
            new_rate = 5

        response = self.client.post(
            '/rate/',
            HTTP_AUTHORIZATION=f'Token {user_token[0].key}',
            data={
                "book": book.id,
                "rate": new_rate
            },
            format='json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['user'], user.id)
        self.assertEqual(response.json()['book'], book.id)
        self.assertEqual(response.json()['rate'], new_rate)
        
    def test_create_rate_fail_with_bad_request(self):
        (user_token, user_id) = get_test_user()
        book_id = create_test_book()
        user = User.objects.get(id=user_id)
        book = Book.objects.get(pk=book_id)
        rate = 10

        response = self.client.post(
            '/rate/',
            HTTP_AUTHORIZATION=f'Token {user_token[0].key}',
            data={
                "book": book.id,
                "rate": rate
            },
            format='json'
        )

        self.assertEqual(response.status_code, 400)
