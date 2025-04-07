from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Question, Answer
from .serializers import QuestionSerializer
from .forms import QuestionForm, AnswerForm
from django.shortcuts import render, redirect

class QuestionListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        questions = Question.objects.all().order_by('-created_at')
        serializer = QuestionSerializer(questions, many=True)
        question_form = QuestionForm()
        answer_form = AnswerForm()
        return render(request, 'feed.html', {
            'questions': serializer.data,
            'question_form': question_form,
            'answer_form': answer_form
        })

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Please log in to post a question."}, status=status.HTTP_401_UNAUTHORIZED)
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            return redirect('question_list_create')
        return render(request, 'feed.html', {
            'questions': Question.objects.all().order_by('-created_at'),
            'question_form': form,
            'answer_form': AnswerForm(),
            'error': form.errors
        })

class AnswerCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, question_id):
        try:
            question = Question.objects.get(id=question_id)
            form = AnswerForm(request.POST)
            if form.is_valid():
                answer = form.save(commit=False)
                answer.user = request.user
                answer.question = question
                answer.save()
                return redirect('question_list_create')
            return render(request, 'feed.html', {
                'questions': Question.objects.all().order_by('-created_at'),
                'question_form': QuestionForm(),
                'answer_form': form,
                'error': form.errors
            })
        except Question.DoesNotExist:
            return Response({"detail": "Question not found."}, status=status.HTTP_404_NOT_FOUND)

class LikeAnswerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, answer_id):
        try:
            answer = Answer.objects.get(id=answer_id)
            if request.user in answer.likes.all():
                answer.likes.remove(request.user)
            else:
                answer.likes.add(request.user)
            return redirect('question_list_create')
        except Answer.DoesNotExist:
            return Response({"detail": "Answer not found."}, status=status.HTTP_404_NOT_FOUND)

class MyQuestionsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        questions = Question.objects.filter(user=request.user).order_by('-created_at')
        serializer = QuestionSerializer(questions, many=True)
        return render(request, 'my_questions.html', {'questions': serializer.data})