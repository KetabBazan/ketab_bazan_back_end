from django.urls import path
from .views import CreateGroup, ShowAllGroups, ShowCategoryGroup

urlpatterns = [
    path('create/', CreateGroup.as_view()),
    path('showall/', ShowAllGroups.as_view()),
    path('showcategorygroups/', ShowCategoryGroup.as_view())
]
