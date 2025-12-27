from django.contrib import admin
from .models import *

# Register your models here.

class QuestionReviewInline(admin.TabularInline):
    model = QuestionReview
    extra = 1
    readonly_fields = ['result', 'answered_at', 'question', 'order', 'level']


class OptionInline(admin.TabularInline):
    model = Option
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'text', 'level', 'pk']
    inlines = [OptionInline]


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ['text', 'question', 'is_correct', 'id']

@admin.register(UserQuizReview)
class UserQuizReviewAdmin(admin.ModelAdmin):
    list_display = ['user']
    inlines = [QuestionReviewInline]

@admin.register(QuestionReview)
class QuestionReviewAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'question']