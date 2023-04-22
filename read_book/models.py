from django.db import models
from django.utils import timezone



class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    name = models.CharField(max_length=200)
    summary = models.TextField(max_length=1000)
    author = models.ManyToManyField(Author, blank=True)
    genre = models.ForeignKey(Genre, blank=True, null=True, on_delete = models.SET_NULL)
    price = models.IntegerField()
    publisher = models.CharField(max_length=50)
    image_url = models.URLField()
    created = models.DateTimeField(default=timezone.now)
    pdf_url = models.URLField(null=True)

    def __str__(self):
        formatter = 'Name: {:28} | Written by: {:8} | Price: {:6}'
        writers = self.getwriters()
        return formatter.format(self.name, writers, self.price)     

    def getwriters(self):
        return "، ".join(str(author) for author in self.author.all())

    def average_rate(self):
        all_rates = [rate.rate for rate in self.rating_set.all()]
        if(len(all_rates)==0): #no one rate for this book
            return 0
        return sum(all_rates)/len(all_rates)

    def allcomments(self):
        all_comments = self.comment_set.all()
        result = []
        i=0
        for comment in all_comments:
            result.append({"id": comment.id,
                           "comment_text": comment.comment_text,
                           "user": comment.user.username,
                           "user_id": comment.user.id,
                           "created_on": comment.created_on,
                           "reply": [],
                           "like": comment.like.count(),
                           "dislike": comment.dislike.count()
                           })
            for reply in comment.replycomment_set.all():
                result[i]['reply'].append({"reply_text": reply.reply_text,
                                           "user": reply.user.username,
                                           "created_on": reply.created_on,
                                           "reply_user_id": reply.user.id
                                           })
            i += 1
        return result

