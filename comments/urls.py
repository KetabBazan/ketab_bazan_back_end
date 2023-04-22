from django.urls import path
from .views import Commentapi, Replytocomment, LikeComment, DislikeComment, UserComments


urlpatterns = [
    path('', Commentapi.as_view()),
    path('reply/', Replytocomment.as_view()),
    path('usercomments/', UserComments.as_view()),
    path('like/', LikeComment.as_view()),
    path('dislike/', DislikeComment.as_view())

]

