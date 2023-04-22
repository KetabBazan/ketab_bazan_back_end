from django.test import TestCase
from rest_framework.test import APITestCase
from accounts.models import User
from comments.tests import get_test_user, create_test_comment
# Create your tests here.



class UserActivityTest(APITestCase):
    def test_user_activity_like_dislike(self):
        (user_token, user_id) = get_test_user()
        comment = create_test_comment(user_id)
        self.client.post('/comment/like/', HTTP_AUTHORIZATION=f'Token {user_token[0].key}',
                         data={'comment_id': comment.id})
        new_comment = create_test_comment(user_id)
        self.client.post('/comment/dislike/', HTTP_AUTHORIZATION=f'Token {user_token[0].key}',
                         data={'comment_id': new_comment.id})
        username = User.objects.get(id=user_id).username
        response = self.client.get(f'/showprofile/allactivity/?username={username}', HTTP_AUTHORIZATION=f'Token {user_token[0].key}')
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'][0]['type'], 'dislike')
        self.assertEqual(response.data['results'][1]['type'], 'like')

