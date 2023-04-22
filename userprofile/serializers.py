from rest_framework import serializers
from .models import Profile
from accounts.models import User

class Profileserializer(serializers.ModelSerializer):
    born_date = serializers.CharField(max_length=12)
    image = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ('fullname', 'bio', 'gender', 'born_date', 'image')

    def get_image(self, obj):
        return "https://api.ketabbazan.ml" + obj.image.url

class Profileserializerwithimage(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('bio', 'gender', 'born_date')


class ProfileImageserializer(serializers.Serializer):
    bio=serializers.CharField(max_length=1000)
    gender=serializers.CharField(max_length=1)
    born_date=serializers.DateField()
    image=serializers.ImageField()

class AccountProfileserializer(serializers.ModelSerializer):
    profile=Profileserializer()
    class Meta:
        model=User
        fields=('username', 'email', 'nickname', 'profile')



