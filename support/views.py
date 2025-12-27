from django.shortcuts import render
from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *


# Create your views here.

class TicketListView(generics.ListAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset.filter(user_id=self.request.user.id)
        return queryset


class TicketCreateView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TicketCreateSerializer(data=request.data)
        if serializer.is_valid():
            subject = serializer.validated_data['subject']
            text = serializer.validated_data['text']
            Ticket.objects.create(user=request.user, subject=subject, text=text)
            return Response('ticket was send!', status=200)
        return Response(serializer.errors)


class AnsweredTicketView(generics.ListAPIView):
    queryset = Ticket.objects.filter(answered=True)
    serializer_class = TicketSerializer

    def get_queryset(self):
        queryset = self.queryset.filter(user_id=self.request.user.id)
        return queryset
