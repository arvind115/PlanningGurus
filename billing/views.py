from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.utils.http import is_safe_url

from .models import BillingProfile, Card

import stripe
STRIPE_API_KEY = getattr(settings,"STRIPE_API_KEY",'sk_test_jcscEC3iRnTzBfAU7jfVf61o00d4ZW7mqH')
STRIPE_PUB_KEY = getattr(settings,"STRIPE_PUB_KEY",'pk_test_QcT5HsC0UoTP1xRhqbC87uFF009NUrh426')

stripe.api_key = STRIPE_API_KEY

def payment_method_view(request,*args,**kwargs):
	billing_profile,created = BillingProfile.objects.new_or_get(request)
	if not billing_profile:
		return redirect('home')
	next_url = ''
	next_ = request.GET.get('next')
	if is_safe_url(next_,request.get_host()):
		next_url = next_
	return render(request,'billing/payment-method.html',{'publish_key':STRIPE_PUB_KEY,'next_url':next_url})

def payment_method_create_view(request,*args,**kwargs):
	# if request.method == 'POST' and request.is_ajax():
	# 	print(request.POST)
	# 	return JsonResponse({'message':'Success! Your card was added'})
	# return HttpResponse('Error')
    if request.method == "POST" and request.is_ajax():
        billing_profile,created = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return HttpResponse({"message": "Cannot find this user"}, status_code=401)
        token = request.POST.get("token")
        if token is not None:
        	print('Token is not NOne')
        	new_card_obj = Card.objects.add_new(billing_profile, token)
        	print('New card created')
        	return JsonResponse({"message": "Success! Your card was added."})
        else:
        	print("Token is NONE. Display Errors")
    return HttpResponse("errors")
