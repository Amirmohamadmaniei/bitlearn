from django.http import HttpResponse
from django.shortcuts import redirect
import requests
import json
from django.core.mail import send_mail
from django.urls import reverse

from BitLearn import settings
from course.models import Subscribe

MERCHANT = '8912c1a0-d4c6-4afe-93ea-58d486486ae5'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
# amount = 11000  # Rial / Required
description = "خرید دوره از سایت بیت لرن"  # Required
# email = 'email@example.com'  # Optional
# mobile = '09123456789'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://localhost:8000/payment/verify/'


def send_request(request):
    total = str(request.user.cart.total_price_with_discount) + '0'
    req_data = {
        "merchant_id": MERCHANT,
        "amount": int(total),
        "callback_url": CallbackURL,
        "description": "خرید دوره از سایت بیت لرن",
        "metadata": {"mobile": request.user.phone, "email": request.user.email}
    }
    req_header = {"accept": "application/json",
                  "content-type": "application/json'"}
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
        req_data), headers=req_header)
    authority = req.json()['data']['authority']
    if len(req.json()['errors']) == 0:
        return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


def verify(request):
    t_status = request.GET.get('Status')
    t_authority = request.GET['Authority']
    if request.GET.get('Status') == 'OK':
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": int(str(request.user.cart.total_price_with_discount) + '0'),
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                courses = request.user.cart.course.all()
                for course in courses:
                    Subscribe.objects.create(course=course, student=request.user)
                    request.user.cart.course.remove(course)

                send_email_success(req.json()['data']['ref_id'], request.user, request.user.email)
                return redirect(reverse('account:profile'))

                # return HttpResponse('Transaction success.\nRefID: ' + str(
                #     req.json()['data']['ref_id']
                # ))
            elif t_status == 101:
                return redirect(reverse('account:profile'))
                # return HttpResponse('Transaction submitted : ' + str(
                #     req.json()['data']['message']
                # ))
            else:
                return redirect(reverse('account:profile'))
                # return HttpResponse('Transaction failed.\nStatus: ' + str(
                #     req.json()['data']['message']
                # ))
        else:
            return redirect(reverse('account:profile'))
            # e_code = req.json()['errors']['code']
            # e_message = req.json()['errors']['message']
            # return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
    else:
        return redirect(reverse('account:profile'))
        # return HttpResponse('Transaction failed or canceled by user')


def send_email_success(refid, user, email):
    subject = 'خرید با موفقیت انجام شد'
    message = f'کد پیگیری خرید شما : \n  code:{refid}'
    email_form = settings.EMAIL_HOST_USER
    ricipient_user = [user, email, ]
    send_mail(subject, message, email_form, ricipient_user)
