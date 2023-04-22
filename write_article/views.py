from write_article.models import Article
from rest_framework import generics, status
from .serializers import ArticleSerializer, ArticleSerializerUpload
from rest_framework.response import Response
from rest_framework import permissions
from write_article.permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView
from jalali_date import datetime2jalali
from show_profile.models import UserActivity


class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.filter(is_verified = True)
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(owner=self.request.user) 
        else:
            return Response(
                data={'message': 'Not Authenticated'},
                status=status.HTTP_401_UNAUTHORIZED
            )            

class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.filter(is_verified = True)
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

class NewestArticles(generics.ListCreateAPIView):
    queryset = Article.objects.filter(is_verified = True).order_by('-created')[0:7]
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]                          

class CreateArticle(APIView):        
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, format=None):
        print(request.data)
        serializer = ArticleSerializerUpload(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            latestarticle = Article.objects.latest('id')
            latestarticle.created_jalali = datetime2jalali(latestarticle.created).strftime('14%y/%m/%d')
            latestarticle.save()
            UserActivity().create(self.request.user, 'article', latestarticle.id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyArticles(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ArticleSerializer

    def get_queryset(self):
        user = self.request.user

        return Article.objects.filter(owner=user)