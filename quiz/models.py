from django.db import models

from accounts.models import User
from read_book.models import Book


class Question(models.Model):
    question = models.CharField(max_length=1000, null=True)
    op1 = models.CharField(max_length=1000, null=True)
    op2 = models.CharField(max_length=1000, null=True)
    op3 = models.CharField(max_length=1000, null=True)
    op4 = models.CharField(max_length=1000, null=True)
    ans = models.IntegerField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.question


class Quiz(models.Model):
    question = models.ManyToManyField(Question, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return "Quiz" + str(self.id)

class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()
    questions_count = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Score :: {str(self.score)} from {str(self.questions_count)} questions"
