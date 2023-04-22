from rest_framework import serializers

from accounts.models import User
from .models import Question, QuizResult, Quiz


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            'question',
            'op1',
            'op2',
            'op3',
            'op4',
            'ans',
            'book',
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'nickname', 'username')
