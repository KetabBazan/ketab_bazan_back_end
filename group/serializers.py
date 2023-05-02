from rest_framework import serializers
from .models import Group
from read_book.models import Genre


class CreateGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', 'bio', 'category', )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'id', )


class ShowGroupSerializer(serializers.ModelSerializer):
    category = GenreSerializer()

    class Meta:
        model = Group
        fields = '__all__'


class UpdateGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', 'bio')
