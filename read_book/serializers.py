from rest_framework import serializers
from django.utils import timezone
from .models import Genre

class BookInfoSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    summary = serializers.CharField(max_length=1000)
    price = serializers.IntegerField()
    publisher = serializers.CharField(max_length=50)
    image_url = serializers.URLField()
    created = serializers.DateTimeField(default=timezone.now) 
    pdf_url = serializers.URLField()  
    genre_name = serializers.CharField(source='genre.name', allow_null=True)

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name',)