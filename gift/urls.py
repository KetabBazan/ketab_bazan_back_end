from django.urls import path
from .views import SendBook, ShowReceivedGift, ShowSendGift, HasUnreadMessage, MarkAllAsRead, MarkMessagesRead

urlpatterns = [
    path('sendbook/', SendBook.as_view()),
    path('allreceivedgifts/', ShowReceivedGift.as_view()),
    path('allsendgifts/', ShowSendGift.as_view()),
    path('hasunread/', HasUnreadMessage.as_view()),
    path('markallread/', MarkAllAsRead.as_view()),
    path('markasread/', MarkMessagesRead.as_view())
]
