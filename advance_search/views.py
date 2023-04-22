from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from read_book.serializers import BookInfoSerializer
from read_book.models import Book
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 100

class Advancesearch(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookInfoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        'name': ['contains'],
        'author__name': ['contains'],
        'genre__name': ['contains'],
        'price': ['gte', 'lte'],
        'publisher': ['contains']
    }
    ordering_fields = [
        'price',
        'created'
    ]
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        objs = super().list(request, *args, **kwargs)
        return objs

