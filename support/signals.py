from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Ticket, TicketAnswer


@receiver(post_save, sender=TicketAnswer)
def change_answer_ticket(sender, instance, **kwargs):
    instance.ticket.answered = True
    instance.ticket.save()