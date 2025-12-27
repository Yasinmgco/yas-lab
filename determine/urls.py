from django.urls import path
from .views import *

urlpatterns = [
    path('test/', GetQuestionView.as_view(), name='tests'),
    path('answer/', SubmitAnswerView.as_view(), name='answer'),
    path('quizzes/', QuizListView.as_view(), name='quizzes'),
    path('quiz-detail/', QuizDetailView.as_view(), name='quiz_detail'),
]