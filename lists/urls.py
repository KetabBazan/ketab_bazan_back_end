from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import force_add_to_list, add_to_list, get_pastread, get_curread, get_leftread, get_favourite, BookStatus
router = DefaultRouter()
router.register('getpastread', get_pastread)
router.register('getcurread', get_curread)
router.register('getleftread', get_leftread)
router.register('getfavourite', get_favourite)


urlpatterns = [
    path('add/', add_to_list.as_view()),
    path('forceadd/', force_add_to_list.as_view()),
    path('bookstatus/', BookStatus.as_view())

]
urlpatterns += router.urls
