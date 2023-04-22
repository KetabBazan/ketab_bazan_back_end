from django.urls import path
from .views import Showprofile, ChangeProfileArticlePublicOrPrivate, ChangeProfileInfoPublicOrPrivate,\
    ChangeProfileReadbookPublicOrPrivate, GetAllActivity

urlpatterns = [
    path('', Showprofile.as_view()),
    path('profileinfo/', ChangeProfileInfoPublicOrPrivate.as_view()),
    path('profilebook/', ChangeProfileReadbookPublicOrPrivate.as_view()),
    path('profilearticle/', ChangeProfileArticlePublicOrPrivate.as_view()),
    path('allactivity/', GetAllActivity.as_view())
]
