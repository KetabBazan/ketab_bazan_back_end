from django.shortcuts import render
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from comments.models import Comment, Replycomment
from rest_framework import status
from comments.serializers import Commentserializer, Allcommentsserializer, Replyserializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from read_book.models import Book
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from show_profile.models import UserActivity
from django.db.models import Q


class Commentapi(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        request.data['user'] = request.user.id
        ser_comment = Commentserializer(data=request.data)
        if ser_comment.is_valid():
            comment = ser_comment.save()
            user_activity = UserActivity()
            user_activity.create(request.user, 'comment', comment.id)
            return Response(ser_comment.data, status=status.HTTP_200_OK)
        else:
            return Response(ser_comment.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        
        book = Book.objects.get(id=request.query_params['id'])
        book_comments = Allcommentsserializer(book)
        return Response(book_comments.data, status=status.HTTP_200_OK)


class Replytocomment(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        request.data['user'] = request.user.id
        ser_reply = Replyserializer(data=request.data)
        if ser_reply.is_valid():
            reply = ser_reply.save()
            user_activity = UserActivity()
            user_activity.create(self.request.user, 'reply', reply.id)
            return Response(ser_reply.data, status=status.HTTP_200_OK)
        else:
            return Response(ser_reply.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        comment_id = request.query_params['comment_id']
        comment = Comment.objects.get(id=comment_id)
        result = []
        for reply in comment.replycomment_set.filter(is_verified=True).all():
            ser_comment = Replyserializer(reply)
            result.append(ser_comment.data)

        return Response(data=result, status=status.HTTP_200_OK)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 10


class UserComments(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = Commentserializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        username = self.request.query_params.get('username')
        return Comment.objects.filter(user__username=username).filter(is_verified=True).order_by('-created_on')[:50]


class LikeComment(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        comment_id = self.request.data.get('comment_id')
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if comment.dislike.all().filter(id=self.request.user.id).exists():
            comment.dislike.remove(self.request.user)
            UserActivity.objects.get(Q(user=self.request.user) & Q(type='dislike') & Q(action_id=comment.id)).delete()
        if comment.like.all().filter(id=self.request.user.id).exists():
            comment.like.remove(self.request.user)
            UserActivity.objects.get(Q(user=self.request.user) & Q(type='like') & Q(action_id=comment.id)).delete()
        else:
            comment.like.add(self.request.user)
            UserActivity().create(self.request.user, 'like', comment.id)
        return Response(status=status.HTTP_200_OK)


class DislikeComment(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        comment_id = self.request.data.get('comment_id')
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if comment.like.all().filter(id=self.request.user.id).exists():
            comment.like.remove(self.request.user)
            UserActivity.objects.get(Q(user=self.request.user) & Q(type='like') & Q(action_id=comment.id)).delete()
        if comment.dislike.all().filter(id=self.request.user.id).exists():
            comment.dislike.remove(self.request.user)
            UserActivity.objects.get(Q(user=self.request.user) & Q(type='dislike') & Q(action_id=comment.id)).delete()
        else:
            comment.dislike.add(self.request.user)
            UserActivity().create(self.request.user, 'dislike', comment.id)
        return Response(status=status.HTTP_200_OK)

