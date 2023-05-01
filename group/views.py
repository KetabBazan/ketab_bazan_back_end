from django.shortcuts import render
from .serializers import CreateGroupSerializer, ShowGroupSerializer
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Group
# Create your views here.


class CreateGroup(CreateAPIView):
    serializer_class = CreateGroupSerializer
    permission_classes = [IsAuthenticated, ]


class ShowAllGroups(ListAPIView):
    serializer_class = ShowGroupSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Group.objects.all()


class ShowCategoryGroup(ListAPIView):
    serializer_class = ShowGroupSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        genre_id = self.request.query_params.get('genre_id')
        return Group.objects.filter(category=genre_id)
