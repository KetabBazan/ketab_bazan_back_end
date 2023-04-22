from django.test import TestCase
from rest_framework.test import APITestCase
from accounts.models import User
from read_book.models import Book, Author, Genre
from rest_framework.authtoken.models import Token
from comments.models import Comment
# Create your tests here.


def get_test_user():
    if User.objects.filter(email='test@test.com').exists():
        user = User.objects.get(email='test@test.com')
    else:
        user = User.objects.create(email='test@test.com', password='test')
    token = Token.objects.get_or_create(user=user)
    return (token, user.id)


def create_test_author():
    author = Author.objects.create(name='test_author')
    return author.id


def create_test_genre():
    genre = Genre.objects.create(name='test_genre')
    return genre.id


def create_test_book():
    author_id = create_test_author()
    genre_id = create_test_genre()
    book = Book.objects.create(name='test_book', genre_id=genre_id, summary='test_summary',
                               price=1000, publisher='test_publisher', image_url='image.com', pdf_url='pdf.com')
    book.author.add(Author.objects.get(id=author_id))
    return book.id


def create_test_comment(user_id):
    book_id = create_test_book()
    comment = Comment.objects.create(comment_text='test', user_id=user_id, book_id=book_id)
    return comment


class CommentLikeTest(APITestCase):

    def test_add_like(self):
        (user_token, user_id) = get_test_user()
        comment = create_test_comment(user_id)
        first_comment_count = comment.like.count()
        response = self.client.post('/comment/like/', HTTP_AUTHORIZATION=f'Token {user_token[0].key}',
                                    data={'comment_id': comment.id})
        self.assertEqual(response.status_code, 200)
        second_comment_count = comment.like.count()
        self.assertEqual(second_comment_count-first_comment_count, 1)
        response = self.client.post('/comment/like/', HTTP_AUTHORIZATION=f'Token {user_token[0].key}',
                                    data={'comment_id': comment.id})
        third_comment_count = comment.like.count()
        self.assertEqual(second_comment_count-third_comment_count, 1)

    def test_add_dislike(self):
        (user_token, user_id) = get_test_user()
        comment = create_test_comment(user_id)
        first_comment_count = comment.dislike.count()
        response = self.client.post('/comment/dislike/', HTTP_AUTHORIZATION=f'Token {user_token[0].key}',
                                    data={'comment_id': comment.id})
        self.assertEqual(response.status_code, 200)
        second_comment_count = comment.dislike.count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(second_comment_count-first_comment_count, 1)
        response = self.client.post('/comment/dislike/', HTTP_AUTHORIZATION=f'Token {user_token[0].key}',
                                    data={'comment_id': comment.id})
        third_comment_count = comment.dislike.count()
        self.assertEqual(second_comment_count - third_comment_count, 1)

    def test_first_like_then_dislike(self):
        (user_token, user_id) = get_test_user()
        comment = create_test_comment(user_id)
        first_comment_like_count = comment.like.count()
        first_comment_dislike_count = comment.dislike.count()
        response = self.client.post('/comment/like/', HTTP_AUTHORIZATION=f'Token {user_token[0].key}',
                                    data={'comment_id': comment.id})
        response = self.client.post('/comment/dislike/', HTTP_AUTHORIZATION=f'Token {user_token[0].key}',
                                    data={'comment_id': comment.id})
        second_comment_like_count = comment.like.count()
        second_comment_dislike_count = comment.dislike.count()
        self.assertEqual(first_comment_like_count, second_comment_like_count)
        self.assertEqual(second_comment_dislike_count-first_comment_dislike_count, 1)