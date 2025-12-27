import datetime

from django.db import models
from User.models import AppUser


# Create your models here.

class QuizSessionManager(models.Manager):
    def get_or_create_active(self, **kwargs):
        instance = self.filter(completed=False, **kwargs).first()
        if instance:
            created = False
        else:
            instance = self.create(**kwargs)
            created = True
        return instance, created


class Level(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=12)
    order = models.IntegerField()

    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.CharField(max_length=212)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=212)
    text_fa = models.CharField(max_length=212)
    objects = models.Manager()

    def __str__(self):
        return f'{self.text}, {self.level}'


class Option(models.Model):
    objects = models.Manager()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=44)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class UserQuizReview(models.Model):
    objects = QuizSessionManager()
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='quiz_reviews')
    order = models.IntegerField(blank=True, null=True)
    score = models.PositiveIntegerField(verbose_name='نمره', blank=True, null=True)
    finished_level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='quizzes', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user}, {self.order}'

    def calculate_score(self):
        questions = self.questions.all()

        lvl_1 = questions.filter(level_id=1, result=True).count()
        lvl_2 = questions.filter(level_id=2, result=True).count()
        lvl_3 = questions.filter(level_id=3, result=True).count()
        lvl_4 = questions.filter(level_id=4, result=True).count()
        lvl_5 = questions.filter(level_id=5, result=True).count()
        false = questions.filter(result=False).count()

        score = (lvl_1 * 1) + (lvl_2 * 2) + (lvl_3 * 3) + (lvl_4 * 4) + (lvl_5 * 5) - (false * 3)
        return score


class QuestionReview(models.Model):
    objects = models.Manager()
    quiz = models.ForeignKey(UserQuizReview, on_delete=models.CASCADE, related_name='questions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_reviews')
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='question_reviews')
    order = models.IntegerField()
    result = models.BooleanField(blank=True, null=True)
    answered_at = models.ForeignKey(Option, on_delete=models.CASCADE, related_name='question_reviews', null=True,
                                    blank=True)

    def __str__(self):
        return f'{self.quiz}, {self.question}'
