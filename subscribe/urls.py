from django.urls import path
# from .views import PlanListView, PaymentView, VerifyPaymentView
from django.urls import path
from . import views

app_name = 'subscribe'


urlpatterns = [
    # path('plans/', PlanListView.as_view(), name='plan-list'),
#     path('pay/', PaymentView.as_view(), name='start-payment'),
#     path('verify/', VerifyPaymentView.as_view(), name='verify-payment'),
]
