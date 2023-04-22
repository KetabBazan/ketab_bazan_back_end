from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from read_book.models import Book
from .serializers import BookInfoSerializer2
from read_book.serializers import BookInfoSerializer
# Create your views here.


def all_books(books):
    ans = []
    for book in books:
        book_serializer = BookInfoSerializer(instance=book)
        data = book_serializer.data
        data['id'] = book.id
        data['author'] = "، ".join(str(author) for author in book.author.all())
        ans.append(data)
    return ans


def check_in_past_read(request, book):
    if request.user.past_read.filter(id=book.id).exists():
        return True
    return False


def check_in_cur_read(request, book):
    if request.user.cur_read.filter(id=book.id).exists():
        return True
    return False


def check_in_favourite(request, book):
    if request.user.favourite.filter(id=book.id).exists():
        return True
    return False


def check_in_left_read(request, book):
    if request.user.left_read.filter(id=book.id).exists():
        return True
    return False


class add_to_list(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        try:
            list_id = request.data['list_id']
        except:
            return Response({"message": "select a list"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            book_id = request.data['book_id']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        book = Book.objects.get(id=book_id)
        if list_id == 1:
            if check_in_cur_read(request, book): return Response({"book_status": 2}, status=status.HTTP_400_BAD_REQUEST)
            if check_in_favourite(request, book): return Response({"book_status": 3}, status=status.HTTP_400_BAD_REQUEST)
            if check_in_left_read(request, book): return Response({"book_status": 4}, status=status.HTTP_400_BAD_REQUEST)
            request.user.past_read.add(book)
        elif list_id == 2:
            if check_in_past_read(request, book): return Response({"book_status": 1}, status=status.HTTP_400_BAD_REQUEST)
            if check_in_favourite(request, book): return Response({"book_status": 3}, status=status.HTTP_400_BAD_REQUEST)
            if check_in_left_read(request, book): return Response({"book_status": 4}, status=status.HTTP_400_BAD_REQUEST)
            request.user.cur_read.add(book)
        elif list_id == 3:
            if check_in_past_read(request, book): return Response({"book_status": 1}, status=status.HTTP_400_BAD_REQUEST)
            if check_in_left_read(request, book): return Response({"book_status": 4}, status=status.HTTP_400_BAD_REQUEST)
            if check_in_cur_read(request, book): return Response({"book_status": 2}, status=status.HTTP_400_BAD_REQUEST)
            request.user.favourite.add(book)
        elif list_id == 4:
            if check_in_past_read(request, book): return Response({"book_status": 1}, status=status.HTTP_400_BAD_REQUEST)
            if check_in_cur_read(request, book): return Response({"book_status": 2}, status=status.HTTP_400_BAD_REQUEST)
            if check_in_favourite(request, book): return Response({"book_status": 3}, status=status.HTTP_400_BAD_REQUEST)
            request.user.left_read.add(book)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        request.user.save()
        return Response(status=status.HTTP_200_OK)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 10


class get_pastread(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookInfoSerializer2
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated, ]
    def get_queryset(self):
        return self.request.user.past_read.all()
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class get_curread(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookInfoSerializer2
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated, ]
    def get_queryset(self):
        return self.request.user.cur_read.all()
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class get_favourite(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookInfoSerializer2
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated, ]
    def get_queryset(self):
        return self.request.user.favourite.all()
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class get_leftread(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookInfoSerializer2
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated, ]
    def get_queryset(self):
        return self.request.user.left_read.all()
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class force_add_to_list(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        try:
            list_id = request.data['list_id']
        except:
            return Response({"message": "select a list"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            book_id = request.data['book_id']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        book = Book.objects.get(id=book_id)
        if list_id == 1:
            request.user.cur_read.remove(book)
            request.user.favourite.remove(book)
            request.user.left_read.remove(book)
            request.user.past_read.add(book)
        elif list_id == 2:
            request.user.past_read.remove(book)
            request.user.favourite.remove(book)
            request.user.left_read.remove(book)
            request.user.cur_read.add(book)
        elif list_id == 3:
            request.user.past_read.remove(book)
            request.user.left_read.remove(book)
            request.user.cur_read.remove(book)
            request.user.favourite.add(book)
        elif list_id == 4:
            request.user.past_read.remove(book)
            request.user.cur_read.remove(book)
            request.user.favourite.remove(book)
            request.user.left_read.add(book)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        request.user.save()
        return Response(status=status.HTTP_200_OK)


class BookStatus(APIView):
    def get(self, request):
        try:
            book_id = request.query_params['book_id']
        except:
            return Response({"message": "no book_id!!"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            Book.objects.get(id=book_id)
        except:
            return Response({"message": "no book with this id"}, status=status.HTTP_400_BAD_REQUEST)
        if request.user.past_read.filter(id=book_id):
            return Response({"list_id": 1}, status=status.HTTP_200_OK)
        elif request.user.cur_read.filter(id=book_id):
            return Response({"list_id": 2}, status=status.HTTP_200_OK)
        elif request.user.favourite.filter(id=book_id):
            return Response({"list_id": 3}, status=status.HTTP_200_OK)
        elif request.user.left_read.filter(id=book_id):
            return Response({"list_id": 4}, status=status.HTTP_200_OK)
        else:
            return Response({"list_id": None}, status=status.HTTP_200_OK)
