from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView

from admin_panel.serializers import CommentSerializer, ArticleSerializer, QuizSerializer
from comments.models import Comment as CommentModel
from write_article.models import Article as ArticleModel
from quiz.models import Quiz as QuizModel


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
        quizzes = QuizModel.objects.order_by('-id').all()[(page - 1) * per_page:page * per_page]
        res = QuizSerializer(quizzes, many=True)

        return Response(res.data, status=status.HTTP_200_OK)


class VerifyQuiz(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request, article_id):
        quiz = QuizModel.objects.get(pk=article_id)
        quiz.is_verified = not quiz.is_verified
        quiz.save()

        res = QuizSerializer(quiz)

        return Response(res.data, status=status.HTTP_200_OK)
