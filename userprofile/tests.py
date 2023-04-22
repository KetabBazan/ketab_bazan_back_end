import requests
from django.test import TestCase
from rest_framework.test import APITestCase
from comments.tests import get_test_user, create_test_comment
from accounts.models import User
# Create your tests here.


class ChangePublicTest(APITestCase):
    def test_change_public_profile_info(self):
        (user_token, user_id) = get_test_user()
        user = User.objects.get(id=user_id)
        self.assertTrue(user.profile.public_profile_info)
        request = self.client.put('/profile/profileinfopublicchange/', HTTP_AUTHORIZATION=f'Token {user_token[0].key}')
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data['message'], 'public profile info is False')
        user = User.objects.get(id=user_id)
        self.assertFalse(user.profile.public_profile_info)
        self.client.put('/profile/profileinfopublicchange/', HTTP_AUTHORIZATION=f'Token {user_token[0].key}')
        user = User.objects.get(id=user_id)
        self.assertTrue(user.profile.public_profile_info)

    def test_change_public_show_articles(self):
        (user_token, user_id) = get_test_user()
        user = User.objects.get(id=user_id)
        self.assertTrue(user.profile.public_show_articles)
        request = self.client.put('/profile/articlespublicchange/', HTTP_AUTHORIZATION=f'Token {user_token[0].key}')
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data['message'], 'public show article is False')
        user = User.objects.get(id=user_id)
        self.assertFalse(user.profile.public_show_articles)
        self.client.put('/profile/articlespublicchange/', HTTP_AUTHORIZATION=f'Token {user_token[0].key}')
        user = User.objects.get(id=user_id)
        self.assertTrue(user.profile.public_show_articles)

    def test_change_public_show_read_books(self):
        (user_token, user_id) = get_test_user()
        user = User.objects.get(id=user_id)
        self.assertTrue(user.profile.public_show_read_books)
        request = self.client.put('/profile/readbookspublicchange/', HTTP_AUTHORIZATION=f'Token {user_token[0].key}')
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data['message'], 'public show read books is False')
        user = User.objects.get(id=user_id)
        self.assertFalse(user.profile.public_show_read_books)
        self.client.put('/profile/readbookspublicchange/', HTTP_AUTHORIZATION=f'Token {user_token[0].key}')
        user = User.objects.get(id=user_id)
        self.assertTrue(user.profile.public_show_read_books)

    def test_change_public_show_activity(self):
        (user_token, user_id) = get_test_user()
        user = User.objects.get(id=user_id)
        self.assertTrue(user.profile.public_show_activity)
        request = self.client.put('/profile/activitypublicchange/', HTTP_AUTHORIZATION=f'Token {user_token[0].key}')
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data['message'], 'public show user activity is False')
        user = User.objects.get(id=user_id)
        self.assertFalse(user.profile.public_show_activity)
        self.client.put('/profile/activitypublicchange/', HTTP_AUTHORIZATION=f'Token {user_token[0].key}')
        user = User.objects.get(id=user_id)
        self.assertTrue(user.profile.public_show_activity)
