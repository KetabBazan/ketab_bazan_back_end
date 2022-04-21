from django.shortcuts import render
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from comments.models import Comment
from rest_framework import status
from comments.serializers import Commentserializer
from rest_framework.permissions import AllowAny


class Commentapi(APIView):
    permission_classes = [AllowAny, ]
    def post(self, request):
        request.data['user'] = request.user.id
        ser_comment = Commentserializer(data=request.data)
        if ser_comment.is_valid():
            ser_comment.save()
            return Response(ser_comment.data, status=status.HTTP_200_OK)
        else:
            return Response(ser_comment.errors, status=status.HTTP_400_BAD_REQUEST)
