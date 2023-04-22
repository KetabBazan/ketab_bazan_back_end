from rest_framework import serializers
from write_article.models import Article
from userprofile.models import Profile
from accounts.models import User

class ArticleSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.nickname')
    owner_id = serializers.ReadOnlyField(source='owner.id')

    image = serializers.SerializerMethodField()
    owner_image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return "https://api.ketabbazan.ml" + obj.image.url

    def get_owner_image(self, obj):
        return "https://api.ketabbazan.ml/profile/getimage/?username=" + obj.owner.username

    class Meta:
        model = Article
        fields = ['id', 'title', 'image', 'book', 'created_jalali', 'body', 'summary', 'owner', 'owner_id', 'owner_image']

class ArticleSerializerUpload(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.nickname')
    owner_id = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Article
        fields = ['id', 'title', 'image', 'book', 'created_jalali', 'body', 'summary', 'owner', 'owner_id']


class ArticleSerializerUserActivity(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'image', 'book', 'summary', 'owner', 'owner_id', 'owner_image']
