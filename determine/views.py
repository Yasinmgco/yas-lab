from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from random import sample
from django.db.models import Count, Max, Func, FloatField
from rest_framework.generics import ListAPIView, RetrieveAPIView


# Create your views here.

class RandomFunc(Func):
    function = 'RANDOM'
    output_field = FloatField()


class GetQuestionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        quiz, created = UserQuizReview.objects.get_or_create_active(user_id=user.id)

        if quiz.order is None:
            last_order = (
                    UserQuizReview.objects.filter(user=user)
                    .exclude(id=quiz.id)
                    .aggregate(max_order=Max('order'))
                    .get('max_order') or 0
            )
            quiz.order = last_order + 1
            quiz.save(update_fields=['order'])

        last_question = (
            quiz.questions.select_related('question')
            .order_by('-order')
            .first()
        )
        if last_question and last_question.result is None:
            serializer = QuestionSerializer(last_question.question)
            return Response({
                "message": "لطفاً ابتدا به سؤال فعلی پاسخ دهید.",
                "quiz_id": quiz.id,
                "question": serializer.data
            })

        level_counts = (
            QuestionReview.objects.filter(quiz=quiz)
            .values('level')
            .annotate(count=Count('id'))
        )
        counts_dict = {c['level']: c['count'] for c in level_counts}

        next_level = None
        for idx, lvl in enumerate(Level.objects.order_by('order')):
            current_count = counts_dict.get(lvl.id, 0)
            if current_count < (2 ** idx) + 2:
                next_level = lvl
                break

        if not next_level:
            return Response({"message": "all levels was completed!"}, status=200)

        question = (
            Question.objects.filter(level=next_level)
            .exclude(question_reviews__quiz=quiz)
            .annotate(rand=RandomFunc())
            .order_by('rand')
            .prefetch_related('options')
            .first()
        )

        if not question:
            return Response({"message": "not any question in this level!"}, status=200)

        last_order = quiz.questions.aggregate(max_order=Max('order'))['max_order'] or 0

        question_review = QuestionReview.objects.create(
            question=question,
            quiz=quiz,
            order=last_order + 1,
            level=next_level
        )

        serializer = QuestionSerializer(question_review.question)
        return Response({'quiz_id': quiz.id, 'question': serializer.data}, status=200)


class SubmitAnswerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            question_review = data['question_review']
            option = data['option']
            quiz = UserQuizReview.objects.get(id=data['quiz_id'])

            question_review.answered_at = option
            question_review.result = option.is_correct
            question_review.save()

            if quiz.questions.filter(result=False).count() >= 3:
                quiz.completed = True
                quiz.score = max(quiz.calculate_score(), 0)
                quiz.finished_level = question_review.level if quiz.score > 5 else None
                quiz.save()
                return Response({"detail": "Quiz Finished!", "score": quiz.score, "level": f"{quiz.finished_level}"},
                                status=200)

            return Response({
                "message": "پاسخ با موفقیت ثبت شد.",
                "result": question_review.result
            }, status=200)
        return Response(serializer.errors, status=400)


class QuizListView(ListAPIView):
    queryset = UserQuizReview.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset.filter(user=self.request.user).order_by('-order')
        return queryset


class QuizDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        quiz_id = request.query_params.get('quiz_id')
        quiz = UserQuizReview.objects.prefetch_related('questions').get(id=quiz_id, user=request.user)
        correct_count = quiz.questions.filter(result=True).count()

        serializer = QuizDetailSerializer(quiz)

        response = {
            'quiz': serializer.data,
            'correct_count': correct_count
        }
        return Response(response)
