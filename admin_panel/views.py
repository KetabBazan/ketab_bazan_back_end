from django.core.exceptions import BadRequest
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView

from admin_panel.permissions import IsSuperAdmin
from admin_panel.serializers import CommentSerializer, ArticleSerializer, QuizSerializer, UserSerializer, QuestionSerializer
from comments.models import Comment as CommentModel
from write_article.models import Article as ArticleModel
from accounts.models import User as UserModel
from quiz.models import Quiz as QuizModel
from quiz.models import Question as QuestionModel

class Comment(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        per_page = 20
        try:
            page = max(1, int(request.query_params['page']))
        except:
            page = 1
        comments = CommentModel.objects.order_by('-id').all()[(page - 1) * per_page:page * per_page]
        res = CommentSerializer(comments, many=True)

        return Response(res.data, status=status.HTTP_200_OK)


class VerifyComment(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request, comment_id):
        comment = CommentModel.objects.get(pk=comment_id)
        comment.is_verified = not comment.is_verified
        comment.save()

        res = CommentSerializer(comment)

        return Response(res.data, status=status.HTTP_200_OK)


class Article(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        per_page = 20
        try:
            page = max(1, int(request.query_params['page']))
        except:
            page = 1
        articles = ArticleModel.objects.order_by('-id').all()[(page - 1) * per_page:page * per_page]
        res = ArticleSerializer(articles, many=True)

        return Response(res.data, status=status.HTTP_200_OK)


class VerifyArticle(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request, article_id):
        article = ArticleModel.objects.get(pk=article_id)
        article.is_verified = not article.is_verified
        article.save()

        res = ArticleSerializer(article)

        return Response(res.data, status=status.HTTP_200_OK)


class Quiz(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        per_page = 20
        try:
            page = max(1, int(request.query_params['page']))
        except:
            page = 1
        quizzes = QuestionModel.objects.order_by('-id').all()[(page - 1) * per_page:page * per_page]
        res = QuestionSerializer(quizzes, many=True)

        return Response(res.data, status=status.HTTP_200_OK)


class VerifyQuiz(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request, quastion_id):
        quiz = QuestionModel.objects.get(pk=quastion_id)
        quiz.is_verified = not quiz.is_verified  
        quiz.save()

        res = QuestionSerializer(quiz)

        return Response(res.data, status=status.HTTP_200_OK)


class User(APIView):
    permission_classes = (IsSuperAdmin,)

    def get(self, request):
        per_page = 20
        try:
            page = max(1, int(request.query_params['page']))
        except:
            page = 1

        users = UserModel.objects.order_by('-id').filter(is_superuser=False).all()[
                (page - 1) * per_page:page * per_page
                ]
        res = UserSerializer(users, many=True)

        return Response(res.data, status=status.HTTP_200_OK)


class UserCahngeRole(APIView):
    permission_classes = (IsSuperAdmin,)

    def post(self, request, user_id):
        user = UserModel.objects.get(pk=user_id)
        if user.is_superuser:
            return Response({"message": "Can not change super admin role"}, status=status.HTTP_400_BAD_REQUEST)
        user.is_staff = not user.is_staff
        user.save()

        res = UserSerializer(user)

        return Response(res.data, status=status.HTTP_200_OK)
