from rest_framework.test import APITestCase
from comments.tests import get_test_user
from accounts.models import User
from quiz.tests import create_test_user


class RootAdminTest(APITestCase):
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

    def test_change_normal_user_to_admin_user(self):
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

        changeable_user = response.json()[0]
        changeable_user_id = changeable_user['id']
        self.assertEqual(changeable_user['is_admin'], False)
        self.assertEqual(changeable_user['is_super_admin'], False)

        response = self.client.post(
            f'/admin-panel/user/change-role/{changeable_user_id}',
            HTTP_AUTHORIZATION=f'Token {user_token[0].key}',
            format='json'
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            '/admin-panel/user/',
            HTTP_AUTHORIZATION=f'Token {user_token[0].key}',
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 20)

        changed_user = response.json()[0]
        print(changed_user)
        self.assertEqual(changed_user['id'], changeable_user_id)
        self.assertEqual(changed_user['is_admin'], True)
        self.assertEqual(changed_user['is_super_admin'], False)

    def test_change_admin_user_to_normal_user(self):
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

        changeable_user = response.json()[0]
        self.assertEqual(changeable_user['is_admin'], False)
        self.assertEqual(changeable_user['is_super_admin'], False)

        changeable_user = User.objects.get(pk=changeable_user['id'])
        changeable_user.is_staff = True
        changeable_user.save()

        response = self.client.post(
            f'/admin-panel/user/change-role/{changeable_user.id}',
            HTTP_AUTHORIZATION=f'Token {user_token[0].key}',
            format='json'
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            '/admin-panel/user/',
            HTTP_AUTHORIZATION=f'Token {user_token[0].key}',
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 20)

        changed_user = response.json()[0]
        self.assertEqual(changed_user['id'], changeable_user.id)
        self.assertEqual(changed_user['is_admin'], False)
        self.assertEqual(changed_user['is_super_admin'], False)
