from django.urls import path
from .views import Advancesearch


urlpatterns = [
    path('', Advancesearch.as_view()),
]


