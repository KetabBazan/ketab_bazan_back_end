from builtins import map

from rest_framework import serializers
from comments.models import Comment
from quiz.models import Quiz, Question
from read_book.models import Book
from accounts.models import User
from write_article.models import Article


class UserCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class BookCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'name')


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'question', 'op1', 'op2', 'op3', 'op4', 'ans')


class CommentSerializer(serializers.ModelSerializer):
    user = UserCommentSerializer(read_only=True)
    book = BookCommentSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    owner = UserCommentSerializer(read_only=True)
    book = BookCommentSerializer(read_only=True)

    class Meta:
        model = Article
        fields = '__all__'


class QuizSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True, many=True)
    book = BookCommentSerializer(read_only=True)

    class Meta:
        model = Quiz
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    is_admin = serializers.BooleanField(default=False, source='is_staff')
    is_super_admin = serializers.BooleanField(default=False, source='is_superuser')

    class Meta:
        model = User
        fields = ('id', 'nickname', 'username', 'email', 'is_admin', 'is_super_admin')
