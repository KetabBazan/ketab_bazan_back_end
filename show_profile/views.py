from django.shortcuts import render
from accounts.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import Publicprofileserializer, UserActivitySerializer
from write_article.models import Article
from rest_framework.permissions import IsAuthenticated
from .models import UserActivity
from rest_framework import generics
from comments.models import Comment, Replycomment
from comments.serializers import Commentserializer, Replyserializer
from write_article.serializers import ArticleSerializerUserActivity
from rest_framework.pagination import PageNumberPagination
# Create your views here.


class Showprofile(APIView):
    def get(self, request):
        try:
            user_username = request.query_params['username']
        except:
            return Response({"message": "no id found!"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=user_username)
        except:
            return Response({"message": "no user with this id"}, status=status.HTTP_400_BAD_REQUEST)
        ser_profile = Publicprofileserializer(user, context={"request":self.request})
        # if not user.profile.public_profile_info:
        #     ser_profile.data['profile'] = 'not public'
        # if not user.profile.public_show_read_books:
        #     ser_profile.data['read_books'] = 'not public'
        # if not user.profile.public_show_articles:
        #     ser_profile.data['user_articles'] = 'not public'
        return Response(ser_profile.data, status=status.HTTP_200_OK)


class ChangeProfileInfoPublicOrPrivate(APIView):
    def put(self, request):
        if request.data['is_public']==1:
            request.user.profile.public_profile_info = True
        else:
            request.user.profile.public_profile_info = False
        request.user.profile.save()
        return Response(status=status.HTTP_200_OK)


class ChangeProfileReadbookPublicOrPrivate(APIView):
    def put(self, request):
        if request.data['is_public'] == 1:
            request.user.profile.public_show_read_books = True
        else:
            request.user.profile.public_show_read_books = False
        request.user.profile.save()
        return Response(status=status.HTTP_200_OK)


class ChangeProfileArticlePublicOrPrivate(APIView):
    def put(self, request):
        if request.data['is_public'] == 1:
            request.user.profile.public_show_articles = True
        else:
            request.user.profile.public_show_articles = False
        request.user.profile.save()
        return Response(status=status.HTTP_200_OK)


class AllActivityOfUser(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        username = self.request.data.get('username')
        results = UserActivity.objects.filter(user__username=username).order_by('-date')[:50]
        pass
        # TODO after talk with frontend team!


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 10


class GetAllActivity(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserActivitySerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        username = self.request.query_params.get('username')
        return UserActivity.objects.filter(user__username=username).order_by('-date')

    def list(self, request, *args, **kwargs):
        responses = super().list(request, *args, **kwargs)
        new_data = responses.data['results']
        for response in new_data:
            activity_type = response['type']
            if activity_type == 'comment' or activity_type == 'like' or activity_type == 'dislike':
                response['detail'] = Commentserializer(Comment.objects.get(id=response['action_id'])).data
            elif activity_type == 'reply':
                response['detail'] = Replyserializer(Replycomment.objects.get(id=response['action_id'])).data
            elif activity_type == 'article':
                response['detail'] = ArticleSerializerUserActivity(Article.objects.get(id=response['action_id'])).data
        responses.data['results'] = new_data
        return responses