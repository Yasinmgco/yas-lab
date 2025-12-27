from rest_framework import serializers
from .models import *


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = '__all__'


class AnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    option_id = serializers.IntegerField()
    quiz_id = serializers.IntegerField()

    def validate(self, data):
        question_id = data['question_id']
        option_id = data['option_id']
        quiz_id = data['quiz_id']

        try:
            question_review = QuestionReview.objects.get(question_id=question_id, quiz_id=quiz_id)
        except QuestionReview.DoesNotExist:
            raise serializers.ValidationError("question not found!")

        if question_review.result is not None:
            raise serializers.ValidationError("you've already answered this question")

        try:
            option = Option.objects.get(pk=option_id, question_id=question_id)
        except Option.DoesNotExist:
            raise serializers.ValidationError("Invalid option")

        data['question_review'] = question_review
        data['option'] = option
        data['quiz_id'] = quiz_id
        return data


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuizReview
        fields = '__all__'


class QuestionReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionReview
        fields = '__all__'


class QuizDetailSerializer(serializers.ModelSerializer):
    questions = QuestionReviewSerializer(many=True, read_only=True)

    class Meta:
        model = UserQuizReview
        fields = "__all__"
