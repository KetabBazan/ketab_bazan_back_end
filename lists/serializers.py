from read_book.serializers import serializers, BookInfoSerializer
from read_book.models import Book

class BookInfoSerializer2(BookInfoSerializer):
    rate = serializers.SerializerMethodField('get_rate')
    author = serializers.SerializerMethodField('get_author')
    id = serializers.SerializerMethodField('get_id')
    class Meta:
        model = Book
        fields = "__all__"
    def get_rate(self,book):
        return book.average_rate()
    def get_author(self, book):
        ans = [author.name for author in book.author.all()]
        return ans
    def get_id(self, book):
        return book.id
