from rest_framework import serializers
from accounts.models import User
from userprofile.serializers import AccountProfileserializer
from write_article.models import Article
from read_book.serializers import BookInfoSerializer
from read_book.models import Book
from comments.models import Comment
from comments.serializers import Commentserializer
from .models import UserActivity
from django.db.models import Q
#from write_article.serializers import ArticleSerializer


class BookInfoSerializer2(BookInfoSerializer):
    rate = serializers.SerializerMethodField('get_rate')
    author = serializers.SerializerMethodField('get_author')
    id = serializers.SerializerMethodField('get_id')
    class Meta:
        model = Book
        fields = "__all__"
    def get_rate(self,book):
        return book.average_rate()
    def get_author(self, book):
        ans = [author.name for author in book.author.all()]
        return ans
    def get_id(self, book):
        return book.id

class ArticleSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.nickname')
    image = serializers.SerializerMethodField()
    owner_image = serializers.SerializerMethodField()
    class Meta:
        model = Article
        fields = ['id', 'title', 'image', 'book', 'created_jalali', 'body', 'summary', 'owner', 'owner_id', 'owner_image']
    def get_image(self, article):
        return "https://api.ketabbazan.ml" + article.image.url
    def get_owner_image(self, article):
        return "https://api.ketabbazan.ml/profile/getimage/?username=" + article.owner.username

class Publicprofileserializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField('get_profile')
    read_books = serializers.SerializerMethodField('get_read_books')
    user_articles = serializers.SerializerMethodField('get_user_articles')
    user_comments = serializers.SerializerMethodField('get_user_comments')

    def get_read_books(self, user):
        if user.profile.public_show_read_books:
            ans = [BookInfoSerializer2(book).data for book in user.past_read.all()]
            return ans
        else:
            return "no public"

    def get_user_articles(self, user):
        if user.profile.public_show_articles:
            ans=ArticleSerializer(Article.objects.filter(owner=user), many=True, context={"request": self.context.get("request")}).data
            return ans
        else:
            return "no public"

    def get_profile(self, user):
        if user.profile.public_profile_info:
            return AccountProfileserializer(user).data
        else:
            return user.username

    def get_user_comments(self, user):
        if user.profile.public_show_activity:
            return Commentserializer(Comment.objects.filter(user=user), many=True).data
        else:
            return "no public"


    class Meta:
        model = User
        fields = ('profile', 'read_books', 'user_articles', 'user_comments')


class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = '__all__'

