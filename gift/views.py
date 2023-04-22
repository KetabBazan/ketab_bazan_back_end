from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import GiftHistorySerializer, ShowGiftSerializer
from rest_framework.generics import ListAPIView
from .models import GiftHistory
from django.db.models import Q
# Create your views here.


class SendBook(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        self.request.data['sender'] = self.request.user.id
        gift_detail = GiftHistorySerializer(data=self.request.data)
        if gift_detail.is_valid():
            gift_detail.save()
            return Response(gift_detail.data, status=status.HTTP_200_OK)
        return Response(data=gift_detail.errors, status=status.HTTP_400_BAD_REQUEST)


class ShowReceivedGift(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ShowGiftSerializer

    def get_queryset(self):
        return GiftHistory.objects.filter(receiver=self.request.user).order_by('-date')


class ShowSendGift(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ShowGiftSerializer

    def get_queryset(self):
        return GiftHistory.objects.filter(sender=self.request.user).order_by('-date')


class HasUnreadMessage(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        result = False
        if GiftHistory.objects.filter(Q(receiver=self.request.user) & Q(is_read=False)).exists():
            result = True
        return Response({"has_unread": result}, status=status.HTTP_200_OK)


class MarkMessagesRead(APIView):
    permission_classes = [IsAuthenticated, ]

    def put(self, request):
        gift_id = self.request.data.get('id')
        try:
            gift_object = GiftHistory.objects.get(Q(id=gift_id) & Q(receiver=self.request.user))
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)
        gift_object.is_read = True
        gift_object.save()
        return Response(status=status.HTTP_200_OK)


class MarkAllAsRead(APIView):
    permission_classes = [IsAuthenticated, ]

    def put(self, request):
        GiftHistory.objects.filter(receiver=self.request.user).update(is_read=True)
        return Response(status=status.HTTP_200_OK)
