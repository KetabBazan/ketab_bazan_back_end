from django.test import TestCase
from rest_framework.test import APITestCase
from read_book.models import Genre
from accounts.models import User
from rest_framework.authtoken.models import Token
from .models import Group
# Create your tests here.


class GroupTest(APITestCase):
    def initial_data(self):
        genre = Genre.objects.get_or_create(name='test_genre')
        self.genre_id = genre[0].id
        self.user = User.objects.get_or_create(email="test@test.com", username="testusername")
        self.token = Token.objects.get_or_create(user=self.user[0])

    def create_groups(self):
        self.initial_data()
        new_genre = Genre.objects.create(name="new_genre")
        self.group1 = Group.objects.create(name="name1", bio="bio1", category_id=self.genre_id, owner_id=self.user[0].id)
        self.group2 = Group.objects.create(name="name2", bio="bio2", category_id=new_genre.id, owner_id=self.user[0].id)

    def test_create_group(self):
        self.initial_data()
        count = Group.objects.count()
        self.assertEqual(0, count)
        request = self.client.post('/groups/create/', HTTP_AUTHORIZATION=f'Token {self.token[0].key}',
                                   data={"name": "test_name", "category": self.genre_id, "bio": "it is bio"},
                                   format='json')
        self.assertEqual(request.status_code, 201)
        self.group = Group.objects.first()
        self.assertEqual(self.group.name, "test_name")
        self.assertEqual(self.group.category.id, self.genre_id)
        self.assertEqual(self.group.owner, self.user[0])
        request = self.client.post('/groups/create/', HTTP_AUTHORIZATION=f'Token {self.token[0].key}',
                                   data={"category": self.genre_id, "bio": "it is bio"},
                                   format='json')
        self.assertEqual(request.status_code, 400)

    def test_show_info(self):
        self.initial_data()
        group = Group.objects.create(id=2, name="name", bio="bio", category_id=self.genre_id, owner=self.user[0])
        request = self.client.get('/groups/showinfo/2', HTTP_AUTHORIZATION=f'Token {self.token[0].key}')
        self.assertEqual(request.status_code, 200)
        self.assertTrue(request.data['name'] == "name")
        self.assertTrue(request.data['bio'] == "bio")
        self.assertTrue(request.data['category']['name'] == "test_genre")
        self.assertTrue(request.data['owner']['username'] == "testusername")

    def test_show_all_groups(self):
        self.create_groups()
        request = self.client.get('/groups/showall/', HTTP_AUTHORIZATION=f'Token {self.token[0].key}')
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.data), 2)
        self.assertEqual(request.data[0]['name'], 'name1')
        self.assertEqual(request.data[0]['category']['name'], 'test_genre')
        self.assertEqual(request.data[0]['owner']['id'], self.user[0].id)
        self.assertEqual(request.data[1]['name'], 'name2')
        self.assertEqual(request.data[1]['category']['name'], 'new_genre')

    def test_show_category_groups(self):
        self.create_groups()
        request = self.client.get(f'/groups/showcategorygroups/?genre_id={self.genre_id}',
                                  HTTP_AUTHORIZATION=f'Token {self.token[0].key}')
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data[0]['name'], 'name1')
        self.assertEqual(request.data[0]['bio'], 'bio1')

    def test_add_member(self):
        self.create_groups()
        # add member
        first_count = self.group1.users.count()
        new_user = User.objects.create(username="add_user", email="add_user@gmail.com")
        self.assertFalse(self.group1.users.filter(username=new_user.username).exists())
        request = self.client.post('/groups/member/', HTTP_AUTHORIZATION=f'Token {self.token[0].key}',
                         data={"group_id": self.group1.id, "new_user_id": new_user.id})
        second_count = self.group1.users.count()
        self.assertEqual(request.status_code, 200)
        self.assertEqual(1, second_count-first_count)
        added_user = self.group1.users.last()
        self.assertEqual(new_user.id, added_user.id)
        self.assertTrue(self.group1.users.filter(id=new_user.id).exists())
        # delete member
        request = self.client.delete('/groups/member/', HTTP_AUTHORIZATION=f'Token {self.token[0].key}',
                                     data={"group_id": self.group1.id, "delete_user_id": new_user.id})
        self.assertEqual(request.status_code, 200)
        third_count = self.group1.users.count()
        self.assertEqual(first_count, third_count)
        self.assertFalse(self.group1.users.filter(id=new_user.id).exists())

    def test_update_info(self):
        self.create_groups()
        request = self.client.put(f'/groups/updateinfo/{self.group1.id}', HTTP_AUTHORIZATION=f'Token {self.token[0].key}'
                                  ,data={"name": "new_name1", "bio": "new_bio1"})
        self.group1 = Group.objects.get(id=self.group1.id)
        self.assertEqual(self.group1.name, "new_name1")
        self.assertEqual(self.group1.bio, "new_bio1")
        self.assertEqual(request.status_code, 200)

