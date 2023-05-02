from django.urls import path
from .views import CreateGroup, ShowAllGroups, ShowCategoryGroup, GroupMembers, UpdateGroupInfo, GroupPhoto

urlpatterns = [
    path('create/', CreateGroup.as_view()),
    path('showall/', ShowAllGroups.as_view()),
    path('showcategorygroups/', ShowCategoryGroup.as_view()),
    path('member/', GroupMembers.as_view()),
    path('updateinfo/<int:pk>', UpdateGroupInfo.as_view()),
    path('photo/', GroupPhoto.as_view())
]
