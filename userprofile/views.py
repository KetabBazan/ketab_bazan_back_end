import os

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import renderer_classes
from rest_framework.views import APIView
from .custom_renders import JPEGRenderer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.models import User
from wsgiref.util import FileWrapper
from rest_framework import generics, viewsets
from .serializers import Profileserializer, Profileserializerwithimage, ProfileImageserializer, AccountProfileserializer
from .models import Profile
# Create your views here.


class Profileimage(generics.RetrieveAPIView):
    renderer_classes = [JPEGRenderer]
    permission_classes = [IsAuthenticated, ]

    def get(self,request):
        image=request.user.profile.image
        return Response(image, content_type='image/jpeg')

    def post(self,request):
        try:
            i=request.FILES['image']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if (request.user.profile.image != "profileimages/default.jpg"):
            os.remove(f"media/profileimages/{request.user.username}.jpg")

        image = request.FILES['image']
        user = User.objects.get(email=request.user.email)
        user.profile.image = image
        user.profile.save()
        os.rename(f"media/profileimages/{image}", f"media/profileimages/{request.user.username}.jpg")
        user.profile.image = f"profileimages/{request.user.username}.jpg"
        user.profile.save()
        return Response(status=status.HTTP_200_OK)


    def delete(self,request):
        if(request.user.profile.image=="profileimages/default.jpg"):
            return Response(data={"message": "default image can not deleted"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            os.remove(f"media/profileimages/{request.user.username}.jpg")
            request.user.profile.image="profileimages/default.jpg"
            request.user.profile.save()
            return Response(data={"message": "image deleted"}, status=status.HTTP_200_OK)


class Profileinfo(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        bio = request.data['bio']
        nickname = request.data['nickname']
        fullname = request.data['fullname']
        request.user.profile.fullname=fullname
        request.user.nickname=nickname
        request.user.profile.bio = bio
        request.user.profile.gender = None
        request.user.profile.born_date = None
        request.user.save()
        request.user.profile.save()
        return Response(status=status.HTTP_200_OK)

    def get(self, request):
        ser_profile = AccountProfileserializer(request.user)
        return Response(ser_profile.data, status=status.HTTP_200_OK)


class UserInfo(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = AccountProfileserializer

    def get_queryset(self):
        username = self.request.query_params.get('username')
        user = User.objects.filter(username=username)
        return user

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        user = self.get_queryset().first()
        if user.profile.public_profile_info:
            return response
        else:
            return Response(data={'message': 'not public profile info'}, status=status.HTTP_403_FORBIDDEN)


class Imageprofile(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        profile=request.user.profile
        ser_profile=ProfileImageserializer(instance=profile)
        return Response({'info': ser_profile.data})


class AccountProfile(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        ser_data = AccountProfileserializer(request.user)
        return Response(ser_data.data, status=status.HTTP_200_OK)


class PasswordChange(APIView):
    permission_classes = [IsAuthenticated, ]
    def post(self, request):
        if (request.user.check_password(request.data['old_password'])):
            request.user.set_password(request.data['new_password'])
            request.user.save()
            return Response(data={"message":"new password set successful"}, status=status.HTTP_200_OK)
        else:
            return Response(data={"message":"old password is wrong"}, status=status.HTTP_400_BAD_REQUEST)

class UsernameChange(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        new_username = request.data['username']
        if(not User.objects.filter(username=new_username).exists() or new_username==request.user.username ):
            request.user.username = new_username
            image = request.user.profile.image
            user = request.user
            os.rename(str(image), f"media/profileimages/{new_username}.jpg")
            user.profile.image = f"media/profileimages/{new_username}.jpg"
            user.profile.save()
            user.save()
            return Response(data={'message':'new username set successful'}, status=status.HTTP_200_OK)
        else:
            return Response(data={'message':'this username already exist'}, status=status.HTTP_400_BAD_REQUEST)

class Profileimagelink(APIView):
    permission_classes = [IsAuthenticated, ]
    renderer_classes = [JPEGRenderer]

    def get(self,request,image_name):
        image=f"media\profileimages\{image_name}"
        return Response(image, content_type='image/jpeg')

class Profileimagefinale(APIView):
    renderer_classes = [JPEGRenderer]
    def get(self, request):
        username = request.query_params['username']
        try:
            user = User.objects.get(username=username)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        image = user.profile.image
        return Response(image, content_type='image/jpeg')


class PublicProfileInfoChange(APIView):
    permission_classes = [IsAuthenticated, ]

    def put(self, request):
        user = self.request.user
        user.profile.public_profile_info = not user.profile.public_profile_info
        user.profile.save()
        return Response(data={"message": f"public profile info is {self.request.user.profile.public_profile_info}"},
                        status=status.HTTP_200_OK)


class PublicShowArticleChange(APIView):
    permission_classes = [IsAuthenticated, ]

    def put(self, request):
        self.request.user.profile.public_show_articles = not self.request.user.profile.public_show_articles
        self.request.user.profile.save()
        return Response(data={"message": f"public show article is {self.request.user.profile.public_show_articles}"},
                        status=status.HTTP_200_OK)


class PublicShowReadBooksChange(APIView):
    permission_classes = [IsAuthenticated, ]

    def put(self, request):
        self.request.user.profile.public_show_read_books = not self.request.user.profile.public_show_read_books
        self.request.user.profile.save()
        return Response(data={"message": f"public show read books is {self.request.user.profile.public_show_read_books}"},
                        status=status.HTTP_200_OK)


class PublicShowActivityChange(APIView):
    permission_classes = [IsAuthenticated, ]

    def put(self, request):
        self.request.user.profile.public_show_activity = not self.request.user.profile.public_show_activity
        self.request.user.profile.save()
        return Response(
            data={"message": f"public show user activity is {self.request.user.profile.public_show_activity}"},
            status=status.HTTP_200_OK)
