from django.urls import path
from .views import Profileimage, Profileinfo, Imageprofile, AccountProfile, PasswordChange,\
    UsernameChange, Profileimagelink, Profileimagefinale, PublicProfileInfoChange, PublicShowArticleChange,\
    PublicShowReadBooksChange, PublicShowActivityChange, UserInfo
from rest_framework.routers import DefaultRouter



urlpatterns = [
    path('image/', Profileimage.as_view()), #main
    path('info/', Profileinfo.as_view()), #main
    path('pimg/', Imageprofile.as_view()),
    path('fullprofile/', AccountProfile.as_view()),
    path('changepassword/', PasswordChange.as_view()), #main
    path('changeusername/', UsernameChange.as_view()), #main
    path('getimage/', Profileimagefinale.as_view()),
    path('profileinfopublicchange/', PublicProfileInfoChange.as_view()),
    path('articlespublicchange/', PublicShowArticleChange.as_view()),
    path('readbookspublicchange/', PublicShowReadBooksChange.as_view()),
    path('activitypublicchange/', PublicShowActivityChange.as_view()),
    path('userinfo/', UserInfo.as_view())
]

