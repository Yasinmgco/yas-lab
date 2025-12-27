from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import generics, viewsets, views
from django.conf import settings
import requests
import json
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import *
from .serializers import PlanSerializer


# Create your views here.


class PlanListView(generics.ListAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer


# ? sandbox merchant
# if settings.SANDBOX:
#     sandbox = 'sandbox'
# else:
#     sandbox = 'www'

# ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
# ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
# ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

amount = 1000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
phone = 'YOUR_PHONE_NUMBER'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8080/verify/'


# class PaymentView(views.APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         user = request.user
#         plan_id = request.data.get("plan_id")
#         phone = request.data.get("phone")
#
#         try:
#             plan = Plan.objects.get(id=plan_id)
#         except Plan.DoesNotExist:
#             return Response({"error": "پلن یافت نشد"}, status=404)
#
#         # ایجاد اشتراک با وضعیت غیرفعال
#         subscription = Subscription.objects.create(user=user, plan=plan, is_active=False)
#
#         # ایجاد پرداخت در حالت pending
#         payment = Payment.objects.create(
#             user=user,
#             subscription=subscription,
#             amount=plan.price,
#             status="pending"
#         )
#
#         data = {
#             "MerchantID": settings.MERCHANT,
#             "Amount": plan.price,
#             "Description": f"خرید اشتراک {plan.name}",
#             "Phone": phone,
#             "CallbackURL": settings.CALLBACK_URL
#         }
#
#         json_data = json.dumps(data)
#         headers = {'content-type': 'application/json', 'content-length': str(len(json_data))}
#
#         response = requests.post(ZP_API_REQUEST, data=json_data, headers=headers)
#         result = response.json()
#
#         if result.get("Status") == 100:
#             payment.authority = result["Authority"]
#             payment.save()
#             return Response({
#                 "payment_url": ZP_API_STARTPAY + result["Authority"],
#                 "authority": result["Authority"]
#             })
#         else:
#             return Response({"error": result}, status=400)
#
#
# class VerifyPaymentView(views.APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         authority = request.GET.get("Authority")
#         status = request.GET.get("Status")
#
#         try:
#             payment = Payment.objects.get(authority=authority)
#         except Payment.DoesNotExist:
#             return Response({"error": "پرداخت یافت نشد"}, status=404)
#
#         if status != "OK":
#             payment.status = "failed"
#             payment.save()
#             return Response({"status": "پرداخت لغو شد"}, status=400)
#
#         data = {
#             "MerchantID": settings.MERCHANT,
#             "Amount": payment.amount,
#             "Authority": authority,
#         }
#         json_data = json.dumps(data)
#         headers = {'content-type': 'application/json', 'content-length': str(len(json_data))}
#
#         response = requests.post(ZP_API_VERIFY, data=json_data, headers=headers)
#         result = response.json()
#
#         if result.get("Status") == 100:
#             payment.status = "success"
#             payment.ref_id = result["RefID"]
#             payment.save()
#
#             # فعال کردن اشتراک
#             subscription = payment.subscription
#             subscription.activate()
#
#             return Response({
#                 "status": "success",
#                 "ref_id": result["RefID"],
#                 "message": "پرداخت موفق و اشتراک فعال شد"
#             })
#         else:
#             payment.status = "failed"
#             payment.save()
#             return Response({"status": "failed", "code": result.get("Status")}, status=400)
