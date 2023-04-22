from django.urls import path
from .views import Booksearch, QuizBooksearch
urlpatterns = [
    path('', Booksearch.as_view()),
    path("quizbook/", QuizBooksearch.as_view()),
]
