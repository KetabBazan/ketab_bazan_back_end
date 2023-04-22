from django.urls import path
#from rest_framework.authtoken.views import obtain_auth_token

from .views import Deposit, UserSignUp, UserLogout, ObtainAuthToken, UserProfile, GetBalance, HasNickName, HasRead, SearchUser

urlpatterns = [
    path('signup/', UserSignUp.as_view()),
    #path('login/', obtain_auth_token),
    path('login/', ObtainAuthToken.as_view()),
    path('profile/', UserProfile.as_view()),
    path('logout/', UserLogout.as_view()),
    path('deposit/', Deposit.as_view()),
    path('balance/', GetBalance.as_view()),
    path('has_nickname/', HasNickName.as_view()),
    path('has_read/<int:book_id>', HasRead.as_view()),
    path('searchuser/', SearchUser.as_view()),
]