from rest_framework import serializers
from .models import Group
from read_book.models import Genre
from accounts.serializers import SearchUserSerializer


class CreateGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', 'bio', 'category', 'owner')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'id', )


class ShowGroupSerializer(serializers.ModelSerializer):
    category = GenreSerializer()
    owner = SearchUserSerializer()
    users = SearchUserSerializer(many=True)
    class Meta:
        model = Group
        fields = '__all__'


class UpdateGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', 'bio')
