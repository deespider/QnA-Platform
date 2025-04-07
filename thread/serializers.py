from rest_framework import serializers
from .models import Question, Answer
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class AnswerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = ['id', 'user', 'content', 'created_at', 'likes_count']

    def get_likes_count(self, obj):
        return obj.likes.count()

class QuestionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'user', 'title', 'created_at', 'answers']