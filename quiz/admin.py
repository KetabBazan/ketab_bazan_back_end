from django.contrib import admin

from .models import Question, Quiz

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    pass
