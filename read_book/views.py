from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Book, Genre
from accounts.models import User
from .serializers import BookInfoSerializer, GenreSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import ListAPIView

class GenreBooks(APIView):
    authentication_classes = []
    permission_classes = []   

    def get(self, request, genre): 
        queryset = Book.objects.filter(genre__name=genre)
        ans = []
        for book in queryset:
            book_serializer = BookInfoSerializer(instance=book)
            data = book_serializer.data
            data['id'] = book.id
            data['author'] = "، ".join(str(author) for author in book.author.all())
            ans.append(data)
        return Response(ans) 

class BuyAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):

        user = User.objects.get(id=request.user.id)

        # Have not enough money
        if Book.objects.get(id=id).price > user.balance:
            return Response("Not Enough Money", status=status.HTTP_402_PAYMENT_REQUIRED)

        # Payed for this book earlier
        if user.purchased_books.filter(id=id).count() > 0:
            return Response("Payed Earlier", status=status.HTTP_304_NOT_MODIFIED)

        user.purchased_books.add(Book.objects.get(id=id))
        #print(user.balance)
        user.balance -= Book.objects.get(id=id).price
        user.save()
        #print(user.balance)

        return Response(data="Success", status=status.HTTP_200_OK)

class AllBooks(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, page = 0):
        books = [book for book in Book.objects.all()]
        books.sort(key = lambda x : x.created, reverse=True)
        ans = []
        iteratingset = books
       # print("page:",page)
        if page == "page_count":
            page_count = len(books) // 16
            if len(books) % 16 > 0:
                page_count += 1
            return Response(page_count)
        if page != 0:
            page = int(page)
            iteratingset = books[(page - 1) * 16 : page * 16]
        for book in iteratingset:
            book_serializer = BookInfoSerializer(instance=book)
            data = book_serializer.data
            data['id'] = book.id
            data['author'] = "، ".join(str(author) for author in book.author.all())
            ans.append(data)
        return Response(ans)    

class NewestBooks(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        books = [book for book in Book.objects.all()]
        books.sort(key = lambda x : x.created, reverse=True)
        ans = []
        for book in books[:10]:
            book_serializer = BookInfoSerializer(instance=book)
            data = book_serializer.data
            data['id'] = book.id
            data['author'] = book.getwriters()
            ans.append(data)
        return Response(ans)

class MostScoreBooks(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        books = [book for book in Book.objects.all()]
        books.sort(key = lambda x : x.average_rate(), reverse=True)
        ans = []
        for book in books[:10]:
            book_serializer = BookInfoSerializer(instance=book)
            data = book_serializer.data
            data['id'] = book.id
            data['author'] = book.getwriters()
            ans.append(data)
        return Response(ans)    

class PDFRetrieval(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        book = get_object_or_404(Book, id=id)  
        if request.user.purchased_books.filter(id=id).count() > 0:
            return Response(book.pdf_url, status=status.HTTP_200_OK)    
        else:
            return Response("Not purchased", status=status.HTTP_400_BAD_REQUEST)

class BookInfoRetrieval(APIView):
    def get(self, request, id):
        book = get_object_or_404(Book, id=id)
        book_serializer = BookInfoSerializer(instance=book)
        data = book_serializer.data
        data['id'] = book.id
        data['author'] = book.getwriters()
        return Response({'book_info': data})


class AllGenres(ListAPIView):
    serializer_class = GenreSerializer

    def get_queryset(self):
        return Genre.objects.all()


class MyPurchasedBooks(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = BookInfoSerializer

    def get_queryset(self):
        return self.request.user.purchased_books.all()


class UserHasBook(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        book_id = self.request.query_params.get('book_id')
        result = False
        if self.request.user.purchased_books.all().filter(id=book_id).exists():
            result = True
        return Response(data={"hasbook": result}, status=status.HTTP_200_OK)
