from django.urls import path
from .views import *

app_name = 'support'
urlpatterns = [
    path('tickets/', TicketListView.as_view(), name='ticket_list'),
    path('answered-tickets/', AnsweredTicketView.as_view(), name='answered_ticket'),
    path('create-ticket/', TicketCreateView.as_view(), name='create_ticket'),
]