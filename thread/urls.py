from django.urls import path
from .views import (QuestionListCreateAPIView, AnswerCreateAPIView, 
                   LikeAnswerAPIView, MyQuestionsAPIView)

urlpatterns = [
    path('', QuestionListCreateAPIView.as_view(), name='question_list_create'),
    path('questions/<int:question_id>/answers/', AnswerCreateAPIView.as_view(), name='answer_create'),
    path('answers/<int:answer_id>/like/', LikeAnswerAPIView.as_view(), name='like_answer'),
    path('my-questions/', MyQuestionsAPIView.as_view(), name='my_questions'),
    # path('logout/', logout_view, name='logout'),
]