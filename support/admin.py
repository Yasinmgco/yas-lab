from django.contrib import admin
from .models import Ticket, TicketAnswer


# Register your models here.


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['subject', 'answered']


@admin.register(TicketAnswer)
class TicketAnswerAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'text']
