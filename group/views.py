from django.shortcuts import render
from .serializers import CreateGroupSerializer, ShowGroupSerializer, UpdateGroupSerializer
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Group
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User
from accounts.serializers import SearchUserSerializer
from userprofile.custom_renders import JPEGRenderer
# Create your views here.


class CreateGroup(CreateAPIView):
    serializer_class = CreateGroupSerializer
    permission_classes = [IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        request.data['owner'] = self.request.user.id
        return super().create(request, *args, **kwargs)


class ShowGroupInfo(RetrieveAPIView):
    serializer_class = ShowGroupSerializer
    queryset = Group.objects.all()


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


class GroupMembers(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        group_id = self.request.data.get('group_id')
        try:
            group = Group.objects.get(id=group_id)
        except:
            return Response(data={"message":"no group with this id"}, status=status.HTTP_400_BAD_REQUEST)
        if group.owner == self.request.user:
            new_user_id = self.request.data.get('new_user_id')
            try:
                new_user = User.objects.get(id=new_user_id)
            except:
                return Response(data={"message":"no user with this id"}, status=status.HTTP_400_BAD_REQUEST)
            group.users.add(new_user)
            group.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(data={"message":"only admin can add"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        group_id = self.request.data.get('group_id')
        try:
            group = Group.objects.get(id=group_id)
        except:
            return Response(data={"message": "no group with this id"}, status=status.HTTP_400_BAD_REQUEST)
        if group.owner == self.request.user:
            delete_user_id = self.request.data.get('new_user_id')
            try:
                new_user = User.objects.get(id=delete_user_id)
            except:
                return Response(data={"message": "no user with this id"}, status=status.HTTP_400_BAD_REQUEST)
            group.users.remove(new_user)
            group.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "only admin can remove"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        group_id = self.request.query_params.get('group_id')
        try:
            group = Group.objects.get(id=group_id)
        except:
            return Response(data={"message": "no group with this id"}, status=status.HTTP_400_BAD_REQUEST)
        response = SearchUserSerializer(group.users.all(), many=True)
        return Response(data=response.data, status=status.HTTP_200_OK)



class UpdateGroupInfo(RetrieveUpdateAPIView):
    serializer_class = UpdateGroupSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Group.objects.all()


class GroupPhoto(APIView):
    #permission_classes = [IsAuthenticated, ]
    renderer_classes = [JPEGRenderer, ]
    def post(self, request):
        group_id = self.request.data['group_id']
        try:
            group = Group.objects.get(id=group_id)
        except:
            return Response(data={"message": "no group with this id"}, status=status.HTTP_400_BAD_REQUEST)
        if self.request.user != group.owner:
            return Response(data={"message":"only admin can set a profile image"}, status=status.HTTP_403_FORBIDDEN)
        image = self.request.FILES.get('image')
        group.picture = image
        group.save()
        return Response(data={"message": "successfully add image"}, status=status.HTTP_200_OK)

    def get(self, request):
        group_id = self.request.query_params.get('group_id')
        try:
            group = Group.objects.get(id=group_id)
        except:
            return Response(data={"message": "no group with this id"}, status=status.HTTP_400_BAD_REQUEST)
        image = group.picture
        return Response(image, content_type='image/jpeg')
