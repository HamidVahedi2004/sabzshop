from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PhoneVerificationForm
from account.models import ShopUser
from cart.common.kavenegar import send_sms_template
from django.contrib.auth import login
import random
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from .forms import *
from django.conf import settings
from django.http import HttpResponse
import requests
import json
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from zibal_payment.client import ZibalClient
from zibal_payment.exceptions import ZibalError
from django.shortcuts import get_object_or_404
import time

# Create your views here.


def verify_phone(request):
    if request.user.is_authenticated:
        return redirect('order:order_create')
    if request.method == "POST":
        form= PhoneVerificationForm(request.POST)
        if form.is_valid():
            phone= form.cleaned_data['phone']
            if ShopUser.objects.filter(phone=phone).exists():
                messages.error(request, 'phone number already registered')
                return redirect('order:verify_phone')
            else:
                tokens= {'token': ''.join(random.choices('0123456789', k=6))}
                request.session['verification_code']= tokens['token']
                request.session['otp_expire']= time.time() + 120
                request.session['phone']= phone
                messages.success(request, f'کد تأیید: {tokens["token"]} (برای تست)')
                print(tokens)
                # send_sms_template('09361465280', tokens, 'send_sms')
                messages.error(request, 'verifycation code send successfully')
                return redirect('order:verify_code')
    else:
        form= PhoneVerificationForm()
    return render(request, 'verify_phone.html', {'form':form})



def verify_code(request):
    if request.method == 'POST':
        code= request.POST.get('code')
        if code:
            verification_code= request.session['verification_code']
            otp_expire= request.session['otp_expire']
            phone= request.session['phone']
            if time.time() <= otp_expire:
                if verification_code == code:
                    user= ShopUser.objects.create_user(phone=phone)
                    user.set_password('123456')
                    user.save()
                    login(request, user)
                    del request.session['verification_code']
                    del request.session['phone']
                    return redirect('order:order_create')
                else:
                    messages.error(request, 'verification code is incorrect')
        
    return render(request, 'verify_code.html')




@login_required
def order_create(request):
    cart = Cart(request)
    last_order = Order.objects.filter(buyer=request.user).order_by('-created').first()
    
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)   # بهتر است commit=False بگذارید تا buyer را اضافه کنید
            order.buyer = request.user
            order.save()
            # ایجاد آیتم‌های سفارش از سبد خرید
            for item in cart:
                Orderitem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                    weight=item['weight']
                )
            request.session['order_id'] = order.id
            return redirect('order:pay')
    else:
        # اگر سفارش قبلی وجود داشت، از آن استفاده کن در غیر این صورت فرم خالی
        if last_order:
            form = OrderCreateForm(instance=last_order)
        else:
            form = OrderCreateForm()   # ✅ اضافه شد

    context = {
        'form': form,
        'cart': cart
    }
    return render(request, 'order_create.html', context)






# #? sandbox merchant 
# if settings.SANDBOX:
#     sandbox = 'sandbox'
# else:
#     sandbox = 'www'


# ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
# ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
# ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"


# CallbackURL = 'http://127.0.0.1:8080/verify/'


# def send_request(request):
#     cart= Cart(request)
#     amount= cart.get_final_price()
#     description=''
#     for item in cart:
#         description += str(item['product'].name) + ", "
#     data = {
#         "MerchantID": settings.MERCHANT,
#         "Amount": amount,
#         "Description": description,
#         "Phone": request.user.phone,
#         "CallbackURL": CallbackURL,
#     }
#     data = json.dumps(data)
#     # set content length by data
#     headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
#     try:
#         response = requests.post(ZP_API_REQUEST, data=data,headers=headers, timeout=10)

#         if response.status_code == 200:
#             response = response.json()
#             if response['Status'] == 100:
#                 return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']), 'authority': response['Authority']}
#             else:
#                 return {'status': False, 'code': str(response['Status'])}
#         return response
    
#     except requests.exceptions.Timeout:
#         return {'status': False, 'code': 'timeout'}
#     except requests.exceptions.ConnectionError:
#         return {'status': False, 'code': 'connection error'}


# def verify(authority):
#     # amount= cart.get_final_price()

#     data = {
#         "MerchantID": settings.MERCHANT,
#         # "Amount": amount,
#         "Authority": authority,
#     }
#     data = json.dumps(data)
#     # set content length by data
#     headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
#     response = requests.post(ZP_API_VERIFY, data=data,headers=headers)

#     if response.status_code == 200:
#         response = response.json()
#         if response['Status'] == 100:
#             return {'status': True, 'RefID': response['RefID']}
#         else:
#             return {'status': False, 'code': str(response['Status'])}
#     return response










# #? sandbox merchant 
# if settings.SANDBOX:
#     sandbox = 'sandbox'
# else:
#     sandbox = 'www'


# ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
# ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
# ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"


# CallbackURL = 'http://127.0.0.1:8080/verify/'


# def send_request(request):
#     cart = Cart(request)
#     amount = cart.get_final_price()
#     description = ''
#     for item in cart:
#         description += str(item['product'].name) + ", "
    
#     data = {
#         "MerchantID": settings.MERCHANT,
#         "Amount": amount,
#         "Description": description,
#         "Phone": request.user.phone,
#         "CallbackURL": CallbackURL,
#     }
#     data = json.dumps(data)
#     headers = {'accept': 'application/json', 'content-type': 'application/json', 'content-length': str(len(data))}
    
#     try:
#         response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)
        
#         if response.status_code == 200:
#             response_json = response.json()
            
#             # بررسی وجود 'Status' در پاسخ
#             if 'Status' not in response_json:
#                 return HttpResponse(f'پاسخ نامعتبر از زرین‌پال: {response_json}')
            
#             if response_json['Status'] == 100:
#                 authority = response_json['Authority']
#                 # ذخیره authority در سشن برای استفاده در verify
#                 request.session['authority'] = authority
#                 request.session['amount'] = amount
#                 return redirect(ZP_API_STARTPAY + authority)
#             else:
#                 # نمایش پیام خطای مناسب بر اساس کد خطا
#                 error_messages = {
#                     101: 'تراکنش قبلاً انجام شده است',
#                     102: 'خطای سیستمی در زرین‌پال',
#                     103: 'خطا در ورودی‌ها',
#                     104: 'MerchantID نامعتبر',
#                 }
#                 error_msg = error_messages.get(response_json['Status'], f'خطا در پرداخت با کد {response_json["Status"]}')
#                 return HttpResponse(f'خطا در اتصال به درگاه پرداخت: {error_msg}')
#         else:
#             return HttpResponse(f'خطا در ارتباط با زرین‌پال. کد وضعیت: {response.status_code}')
            
#     except requests.exceptions.Timeout:
#         return HttpResponse('خطا: زمان اتصال به درگاه پرداخت به پایان رسید')
#     except requests.exceptions.ConnectionError:
#         return HttpResponse('خطا: مشکل در اتصال به اینترنت یا درگاه پرداخت')
#     except Exception as e:
#         return HttpResponse(f'خطای ناشناخته: {str(e)}')
    
    
# def verify(authority):
#     data = {
#         "MerchantID": settings.MERCHANT,
#         # "Amount": amount,
#         "Authority": authority,
#     }
#     data = json.dumps(data)
#     # set content length by data
#     headers = {'accept': 'application/json', 'content-type': 'application/json', 'content-length': str(len(data))}
#     try:
#         response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
#         if response.status_code == 200:
#             response_json = response.json()
#             reference_id = response_json['RefID']
#             if response['Status'] == 100:
#                 return HttpResponse(f'successful , RefID: {reference_id}')
#             else:
#                 return HttpResponse('Error')
#         return HttpResponse('response failed')
#     except requests.exceptions.Timeout:
#         return HttpResponse('Timeout Error')
#     except requests.exceptions.ConnectionError:
#         return HttpResponse('Connection Error')



# ========================
# تنظیمات اولیه (Sandbox)
# ========================\
SANDBOX= True
MERCHANT_ID = 'zibal'  # برای تست
CALLBACK_URL = 'http://127.0.0.1:8000/verify/'  # آدرس بازگشت (حتماً / در آخر داشته باشد)

def send_payment_request(request):
    order= get_object_or_404(Order, id= request.session['order_id'], buyer= request.user)
    amount_rial = order.get_finel_cost() # مبلغ به ریال
    description= ''
    for item in order.items.all():
        description += str(item.product.name) + ", "
    try:
        # راه‌اندازی کلاینت با حالت sandbox
        client = ZibalClient(merchant_id=MERCHANT_ID, sandbox=True)
        
        # ارسال درخواست پرداخت
        response = client.payment_request(
            amount=amount_rial,
            callback_url=CALLBACK_URL,
            description=description
        )
        
        track_id = response.get("trackId")
        payment_url = client.generate_payment_url(track_id)
        
        # هدایت کاربر به صفحه پرداخت
        return redirect(payment_url)
        
    except ZibalError as e:
        return JsonResponse({"error": f"خطا در درخواست پرداخت: {e}"}, status=400)
    
    
    
@csrf_exempt  # برای دریافت بازگشت از درگاه
def verify_payment(request):
    order= Order.objects.get(id= request.session['order_id'])
    if request.method == 'GET':
        track_id = request.GET.get('trackId')
        success = request.GET.get('success')
        
        if success == '1' and track_id:
            try:
                client = ZibalClient(merchant_id=MERCHANT_ID, sandbox=True)
                verification = client.payment_verify(track_id)
                
                if verification.get('result') == 100:
                    order.paid = True
                    order.save()
                    
                    Transaction.objects.create(
                        order=order, 
                        price= order.get_finel_cost(),
                        status= 'success'
                    ) 
                    
                    for item in order.items.all():
                        item.product.inventory -= item.quantity
                        item.product.save()
                    # پرداخت موفق
                    context={
                        "success": True,
                        "ref_number": verification.get('refNumber'),
                        "card_number": verification.get('cardNumber'),
                        "order_id": order.id,
                        "amount": verification.get('amount')
                    }
                    return render(request, 'payment-tracking.html', context)
                else:
                    return JsonResponse({"success": False, "message": "پرداخت ناموفق"}, status=400)
                    
            except ZibalError as e:
                return JsonResponse({"success": False, "message": str(e)}, status=500)
                
    return JsonResponse({"success": False}, status=400)




def order_list(request):
    user= request.user
    orders= Order.objects.filter(user=user)
    return render(request, 'order_list.html', {'orders':orders})


@login_required
def order_detail(request, id):
    order= get_object_or_404(Order, id= id, buyer= request.user)
    return render(request, 'order_detail.html', {'order':order})