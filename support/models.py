from django.db import models
from User.models import AppUser


# Create your models here.


class Ticket(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, verbose_name='کاربر')
    subject = models.CharField(max_length=220, verbose_name='موضوع')
    text = models.TextField(verbose_name='متن تیکت')
    created = models.DateTimeField(auto_now_add=True)
    answered = models.BooleanField(verbose_name='پاسخ داده شده/نشده', default=False)

    def __str__(self):
        return f'{self.user},{self.subject}'


class TicketAnswer(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.ticket} answer'
