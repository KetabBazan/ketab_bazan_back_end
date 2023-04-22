from django.urls import path

from admin_panel.views import Comment, VerifyComment, Article, VerifyArticle, Quiz, VerifyQuiz, User, UserCahngeRole

urlpatterns = [
    path('comment/', Comment.as_view()),
    path('comment/verify/<int:comment_id>', VerifyComment.as_view()),
    path('article/', Article.as_view()),
    path('article/verify/<int:article_id>', VerifyArticle.as_view()),
    path('quiz/', Quiz.as_view()),
    path('quiz/verify/<int:article_id>', VerifyQuiz.as_view()),
    path('user/', User.as_view()),
    path('user/change-role/<int:user_id>', UserCahngeRole.as_view()),
]
