from django.urls import path

from . import views

urlpatterns = [
    path('propose/', views.ProposeQuestion.as_view()),
    path('generate/<int:book_id>', views.GenerateQuiz.as_view()),
    path('submit/<int:quiz_id>', views.SubmitQuiz.as_view()),
    path('best-scores/', views.BestScores.as_view())
]
