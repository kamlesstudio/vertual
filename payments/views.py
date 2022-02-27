# from django.shortcuts import redirect, render
# from . import Checksum
# from django.shortcuts import render
# from django.conf import settings
# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from payments.utils import VerifyPaytmResponse
# import requests
# from django.contrib import messages
# from users.forms import MessageForm
from django.contrib import messages
from django.http.response import JsonResponse
from . import Checksum
from django.shortcuts import redirect, render
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import VerifyPaytmResponse
import requests
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return HttpResponse("<html><a href='payment'>PayNow</html>")


def payment(request):
    user = request.user
    print(user)
    order_id = Checksum.__id_generator__()
    bill_amount = "1"
    data_dict = {
        'MID': settings.PAYTM_MERCHANT_ID,
        'INDUSTRY_TYPE_ID': settings.PAYTM_INDUSTRY_TYPE_ID,
        'WEBSITE': settings.PAYTM_WEBSITE,
        'CHANNEL_ID': settings.PAYTM_CHANNEL_ID,
        'CALLBACK_URL': settings.PAYTM_CALLBACK_URL,
        'MOBILE_NO': '8528933970',
        'EMAIL': 'kamleshlovesu@gmail.com',
        'CUST_ID': '123321',
        'ORDER_ID':order_id,
        'TXN_AMOUNT': bill_amount,
        
    } # This data should ideally come from database
    data_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict, settings.PAYTM_MERCHANT_KEY)
    
    print('data-dict',data_dict)
    print(settings.PAYTM_PAYMENT_GATEWAY_URL)
    print( settings.PAYTM_COMPANY_NAME)
    context = {
        'payment_url': settings.PAYTM_PAYMENT_GATEWAY_URL,
        'comany_name': settings.PAYTM_COMPANY_NAME,
        'data_dict': data_dict,
        'user':user
        
    }
    return render(request, 'payments/payment.html', context)


@csrf_exempt
def response(request):
    user = request.user
    print(user)
    print('res',request.POST)
    resp = VerifyPaytmResponse(request)
    if resp['verified']:
        # save success details to db; details in resp['paytm']
        messages.success(request,'Transaction Successful')
        return JsonResponse('hi')
    else:
        # check what happened; details in resp['paytm']
        messages.error(request,"Transaction Failed")
    return redirect('create-message',user.id)