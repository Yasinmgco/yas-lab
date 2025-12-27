from rest_framework import serializers
from .models import *


class TicketAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketAnswer
        fields = ['text', 'created']


class TicketSerializer(serializers.ModelSerializer):
    answers = TicketAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = ['text', 'subject', 'answered', 'created', 'user', 'answers']


class TicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['subject', 'text']
