import random

import requests
from django.test import TestCase
from rest_framework.test import APITestCase
from comments.tests import get_test_user, create_test_book
from accounts.models import User

# Create your tests here.
from read_book.models import Book


class AdvancedSearchTest(APITestCase):
    def test_create_and_update_rate(self):
        (user_token, user_id) = get_test_user()

        books = []
        for i in range(10):
            books.append(create_test_book())

        response = self.client.get(
            '/advancesearch/',
            HTTP_AUTHORIZATION=f'Token {user_token[0].key}',
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()['results']) <= len(books))

        equal_count = len(response.json()['results'])
        for response_book in response.json()['results']:
            for book in books:
                if book.id == response_book['id']:
                    equal_count -= 1

        self.assertEqual(equal_count, 0)
