from django.test import TestCase
from rest_framework.test import APITestCase
from accounts.models import User
from comments.tests import create_test_book
from read_book.models import Book
from rest_framework.authtoken.models import Token
from .models import GiftHistory
# Create your tests here.


class GiftTest(APITestCase):

    def initial_data(self):
        self.sender_user = User.objects.get_or_create(email="sender@gmail.com", password='1234', username='sender')[0]
        self.receiver_user = User.objects.get_or_create(email="receiver@gmail.com", password='1234', username='receiver')[0]
        self.sender_token = Token.objects.get_or_create(user=self.sender_user)
        self.book_id = create_test_book()

    def test_send_gift_normal(self):
        self.initial_data()
        self.sender_user.purchased_books.add(Book.objects.get(id=self.book_id))
        response = self.client.post('/gift/sendbook/', HTTP_AUTHORIZATION=f'Token {self.sender_token[0].key}',
                                    data={"receiver": self.receiver_user.id, "book": self.book_id},
                                    format='json')
        self.assertEqual(response.status_code, 200)
        gift_object = GiftHistory.objects.last()
        self.assertEqual(gift_object.sender, self.sender_user)
        self.assertEqual(gift_object.receiver, self.receiver_user)
        self.assertTrue(self.receiver_user.purchased_books.all().filter(id=self.book_id).exists())
        self.assertFalse(self.sender_user.purchased_books.all().filter(id=self.book_id).exists())

    def test_send_gift_sender_does_not_have_book(self):
        self.initial_data()
        self.sender_user.purchased_books.remove(self.book_id)
        response = self.client.post('/gift/sendbook/', HTTP_AUTHORIZATION=f'Token {self.sender_token[0].key}',
                                    data={"receiver": self.receiver_user.id, "book": self.book_id},
                                    format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['non_field_errors'][0], "you dont have this book")
        self.assertFalse(self.sender_user.purchased_books.all().filter(id=self.book_id).exists())
        self.assertFalse(self.receiver_user.purchased_books.all().filter(id=self.book_id).exists())

    def test_send_gift_receiver_has_book(self):
        self.initial_data()
        self.sender_user.purchased_books.add(self.book_id)
        self.receiver_user.purchased_books.add(self.book_id)
        response = self.client.post('/gift/sendbook/', HTTP_AUTHORIZATION=f'Token {self.sender_token[0].key}',
                                    data={"receiver": self.receiver_user.id, "book": self.book_id},
                                    format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['non_field_errors'][0], "receiver already has this book")
        self.assertTrue(self.sender_user.purchased_books.all().filter(id=self.book_id).exists())
        self.assertTrue(self.receiver_user.purchased_books.all().filter(id=self.book_id).exists())

    def test_send_gift_circulary(self):
        self.initial_data()
        self.sender_user.purchased_books.add(self.book_id)
        self.receiver_user.purchased_books.remove(self.book_id)
        self.client.post('/gift/sendbook/', HTTP_AUTHORIZATION=f'Token {self.sender_token[0].key}',
                         data={"receiver": self.receiver_user.id, "book": self.book_id},
                         format='json')
        receiver_token = Token.objects.get_or_create(user=self.receiver_user)
        response = self.client.post('/gift/sendbook/', HTTP_AUTHORIZATION=f'Token {receiver_token[0].key}',
                         data={"receiver": self.sender_user.id, "book": self.book_id},
                         format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['non_field_errors'][0], "You can send this book to this user because"
                                                               " he send it to you as a gift")
        self.assertFalse(self.sender_user.purchased_books.all().filter(id=self.book_id).exists())
        self.assertTrue(self.receiver_user.purchased_books.all().filter(id=self.book_id).exists())

    def test_all_sended_gifts(self):
        self.initial_data()
        self.sender_user.purchased_books.add(Book.objects.get(id=self.book_id))
        self.receiver_user.purchased_books.remove(self.book_id)
        self.client.post('/gift/sendbook/', HTTP_AUTHORIZATION=f'Token {self.sender_token[0].key}',
                                    data={"receiver": self.receiver_user.id,
                                          "book": self.book_id,
                                          "message": "this book for you"},
                                                           format='json')
        response = self.client.get('/gift/allsendgifts/', HTTP_AUTHORIZATION=f'Token {self.sender_token[0].key}')
        self.assertEqual(len(response.data), 1)
        gift_obj = response.data[0]
        self.assertFalse(gift_obj['is_read'])
        self.assertEqual(gift_obj['message'], 'this book for you')
        self.assertEqual(gift_obj["book"]['name'], 'test_book')

    def test_is_read_apis(self):
        self.initial_data()
        self.sender_user.purchased_books.add(Book.objects.get(id=self.book_id))
        self.receiver_user.purchased_books.remove(self.book_id)
        self.client.post('/gift/sendbook/', HTTP_AUTHORIZATION=f'Token {self.sender_token[0].key}',
                         data={"receiver": self.receiver_user.id,
                               "book": self.book_id,
                               "message": "this book for you"},
                         format='json')
        receiver_token = Token.objects.get_or_create(user=self.receiver_user)
        response = self.client.get('/gift/hasunread/', HTTP_AUTHORIZATION=f'Token {receiver_token[0].key}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['has_unread'], True)
        gift_object = GiftHistory.objects.last()
        response = self.client.put('/gift/markasread/', HTTP_AUTHORIZATION=f'Token {receiver_token[0].key}',
                        data={'id': gift_object.id})
        self.assertEqual(response.status_code, 200)
        gift_object = GiftHistory.objects.last()
        self.assertTrue(gift_object.is_read)
        gift_object = GiftHistory.objects.last()
        gift_object.is_read = False
        gift_object.save()
        response = self.client.put('/gift/markasread/', HTTP_AUTHORIZATION=f'Token {receiver_token[0].key}',
                                   data={'id': gift_object.id})
        self.assertEqual(response.status_code, 200)
        gift_object = GiftHistory.objects.last()
        self.assertTrue(gift_object.is_read)

