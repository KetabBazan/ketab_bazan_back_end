import random

import requests
from django.test import TestCase
from rest_framework.test import APITestCase
from comments.tests import get_test_user, create_test_book
from accounts.models import User

# Create your tests here.
from quiz.models import Quiz, QuizResult
from read_book.models import Book


def create_test_quiz():
    quiz = Quiz.objects.create()
    return quiz


def create_test_quiz_result(user_id, quiz_id):
    quiz_result = QuizResult.objects.create(
        user_id=user_id,
        quiz_id=quiz_id,
        score=random.randint(0, 100),
        questions_count=random.randint(0, 10),
    )
    return quiz_result


def create_test_user():
    rand_int = str(random.randint(1, 1000))
    try:
        user = User.objects.get(
            username=rand_int,
        )
    except:
        user = None
    while user is not None:
        rand_int = str(random.randint(1, 1000))
        try:
            user = User.objects.get(
                username=rand_int,
            )
        except:
            user = None
    user = User.objects.create(
        username=rand_int,
        email=f'{rand_int}@test.com',
        password='test'
    )
    return user


class QuizResultTest(APITestCase):
    def test_best_scores(self):
        users = []
        for i in range(10):
            user = create_test_user()
            users.append(User.objects.get(id=user.id))
        quiz = create_test_quiz()
        for user in users:
            quiz_result = create_test_quiz_result(
                user_id=user.id,
                quiz_id=quiz.id
            )

        response = self.client.get(
            '/quiz/best-scores/',
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        print(len(response.json()) == 10)
        # self.assertEqual(response.json()['user'], user.id)
