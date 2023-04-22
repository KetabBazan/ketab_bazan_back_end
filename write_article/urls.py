from django.urls import path
from .views import ArticleList, ArticleDetail, CreateArticle, MyArticles, NewestArticles

app_name = 'write_article'

urlpatterns = [
    path('', ArticleList.as_view()),
    path('<int:pk>/', ArticleDetail.as_view()),
    path('newest_articles/', NewestArticles.as_view()),
    path('create_article/', CreateArticle.as_view()),
    path('my_articles/', MyArticles.as_view())
]