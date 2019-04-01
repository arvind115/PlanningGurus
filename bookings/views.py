from django.conf import settings
from django.shortcuts import render,redirect,get_object_or_404,render_to_response
from django.http import Http404
from django.contrib import messages
from .models import Booking, Detail
from .forms import BookingForm,CityForm,EventForm, DetailForm
from accounts.forms import LoginForm

from orders.models import Order
from events.models import Event 
from cities.models import City
from emfs.models import Emf
from billing.models import BillingProfile

import stripe
STRIPE_API_KEY = getattr(settings,"STRIPE_API_KEY",'sk_test_jcscEC3iRnTzBfAU7jfVf61o00d4ZW7mqH')
STRIPE_PUB_KEY = getattr(settings,"STRIPE_PUB_KEY",'pk_test_QcT5HsC0UoTP1xRhqbC87uFF009NUrh426')

stripe.api_key = STRIPE_API_KEY


def emf_and_event(booking):
	'''returns True if Emf associated with current Booking instance organises the associated Event'''
	if booking.emf is not None and booking.event is not None:
		return booking.event in booking.emf.events.all()
def emf_and_city(booking):
	'''returns True if Emf associated with current Booking instance operates in the associated City'''
	if booking.city is not None and booking.emf is not None:
		return booking.emf in booking.city.emf.all()

def booking_view(request,*args,**kwargs):
	print('\n\t\tin BOOKING VIEW\n')
	booking_obj,created = Booking.objects.new_or_get(request)
	context={ 'booking_obj':booking_obj }
	event_slug = kwargs.get('event',None)
	if event_slug is not None: #arrived from HOME page link or the bookings:home
		event = Event.objects.get(slug=event_slug)
		booking_obj.event = event
		booking_obj.save()                     ### move all the save/update logic to booking.models ASAP
		##above save method runs even when the event object is same. ONLY save when its different or None
		data={'city':booking_obj.city,'event':event}
		context['form']     = BookingForm(initial=data)
		#The city may still be there. Consider that too.
		if booking_obj.city is not None:
			context['queryset'] = booking_obj.city.emf.all().filter(events__event__icontains=event.event)
		else: #consider only the event if city is blank
			context['queryset'] = event.emf_set.all().filter()
		return render(request,"bookings/booking.html",context)
	form = BookingForm(request.POST or None) #arrived from the bookings:booking page itself
	date = request.POST.get('booking_date',None)
	if date is not None and len(date):
		booking_obj.booking_date = date
		booking_obj.save()
		##above save method runs even when the date is same. ONLY save when its different or None
	context['form'] = form
	city_id = request.POST.get('city',None) #this is coming from the BookingForm
	eventid = request.POST.get('event',None) #this is coming from the BookingForm
	context['city_set_present'],cityset = False,None
	context['event_set_present'],eventset = False,None
	if city_id is not None and len(city_id):
		city_obj = City.objects.get(id=city_id)
		booking_obj.city = city_obj
		booking_obj.save()
		##above save method runs even when the city object is same. ONLY save when its different or None
		cityset = city_obj.emf.all()
		if cityset.count():
			context['cqs']  = cityset
			context['city_set_present'],context['no_result'] = True,False
	if eventid is not None and len(eventid):
		event = get_object_or_404(Event,id=eventid) #get the event object from event.id
		context['event']  = event
		booking_obj.event = event
		booking_obj.save()
		##above save method runs even when the event object is same. ONLY save when its different or None
		eventset = event.emf_set.all() #emfs that do the event
		if eventset.count():
			context['eqs']  = eventset # event queryset
			context['event_set_present'],context['no_result'] = True,False
	if city_id is not None and eventid is not None: #both are there
		if eventset is not None and cityset is not None:
			# queryset = eventset | cityset
			queryset = cityset.filter(events__event__icontains=event.event)
			if queryset.count(): #both present
				context['queryset'] = queryset.distinct()
				context['both'] = True
				del eventset,cityset #free up some memory
				del context['eqs'],context['cqs']  
	return render(request,"bookings/booking.html",context)

def booking_home(request,*args,**kwargs):
	print('\n\t\tin booking HOME\n')
	booking_obj,created = Booking.objects.new_or_get(request) #return a booking object if already exists or creates a new one.	
	form = CityForm(request.POST or None)
	eform = EventForm(request.POST or None)
	context={
		'booking_obj':booking_obj,
		'form':form,
		'eform':eform,
	}
	if booking_obj.event is not None and booking_obj.emf is not None:
		if not emf_and_event(booking_obj):
			context['warning'] = True
	if booking_obj.emf is not None and booking_obj.city is not None:
		if not emf_and_city(booking_obj): #city warning
			context['cwarning'] = True
	return render(request,'bookings/bookinghome.html',context)

def booking_update(request):# del request.session['booking_obj']
	print('\n\t\tin booking UPDATE\n')
	print('POST: ',request.POST)
	booking_obj, created = Booking.objects.new_or_get(request) #get the current BOOKING object, or create a new one.
	if request.method == "POST":
		city_id 	= request.POST.get('city_id')
		event_id 	= request.POST.get('event_id')
		emf_id 		= request.POST.get('emf_id')   
		if city_id is not None and len(city_id):
			city 	= City.objects.get(id=city_id)
			print('getting the city id::',city)
			booking_obj.city = city #add the city
		else:
			city_id = request.POST.get('city') #coming from bookings:update
			if city_id is not None and len(city_id):
				city = City.objects.get(id=city_id) #get the city
				if booking_obj.city == city: #need to remove
					booking_obj.city = None
				else: #need to add
					booking_obj.city = city
		if event_id is not None and len(event_id):
			event 	= Event.objects.get(id=event_id)
			print("getting the Event id::",event)
			booking_obj.event = event #add the event
		else: #coming from bookings:update
			event_id = request.POST.get('event')
			if event_id is not None and len(event_id):
				event = Event.objects.get(id=event_id)
				if booking_obj.event == event: #need to remove
					booking_obj.event = None
				else: #need to add
					booking_obj.event = event
		if emf_id is not None and len(emf_id):
			emf 	= Emf.objects.get(id=emf_id)
			print('getting the Emf id::',emf)
			booking_obj.emf = emf #add the emf
		else: #coming from 'bookings:update'
			emf_id = request.POST.get('emf')
			if emf_id is not None and len(emf_id):
				emf = Emf.objects.get(id=emf_id)
				if booking_obj.emf == emf: #need to remove
					booking_obj.emf = None
				else:
					booking_obj.emf = emf
		booking_obj.save()
	else:
		print("\n\tNOT a POST request\n")
	return redirect('bookings:home')

def detail_view(request,*args,**kwargs):
	form = DetailForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		decor = form.cleaned_data.get('decor',None)
		people = form.cleaned_data.get('people',0)
		photography = form.cleaned_data.get('photography',None)
		dj = form.cleaned_data.get('DJ_Entertainment',None)
		l = [v is not None for (k,v) in form.cleaned_data.items()]
		if all(l): #attach the details to the Booking
			# detail = Detail.objects.create(decor=decor,people=int(people),photography=photography,DJ_Entertainment=dj)
			booking_obj,created = Booking.objects.new_or_get(request)
			booking_obj.details.decor=decor
			booking_obj.details.people=int(people)
			booking_obj.details.photography=photography,
			booking_obj.details.DJ_Entertainment=dj 
			booking_obj.save()
			# billing_profile,created = BillingProfile.objects.new_or_get(request)
			print('redirecting to checkout form detail_view')
			return redirect('bookings:checkout')# if necessary details have been filled, redirect to 'bookings:checkout'
	context={
		'form':form,
	}
	return render(request,'bookings/details.html',context)

def checkout(request,*args,**kwargs):
	print('\n\t\tin CHECKOUT\n')
	#get the Booking object from the session
	booking_obj,created = Booking.objects.new_or_get(request)
	order_obj = None
	login_form = LoginForm()
	#get the BillingProfile, if the user is  logged in, else a None profile
	billing_profile,created = BillingProfile.objects.new_or_get(request)
	if billing_profile is not None: #we have a billing_profile
		order_obj,created = Order.objects.new_or_get(billing_profile,booking_obj)
		print('billing_profile:: ',billing_profile)
		if order_obj is not None:
			print('Order_obj::',order_obj)
		else:
			print('\n\t\tOrder_obj is None\n')
	else:
		print('\n\t\tbilling_profile is None\n')
	if request.method == 'POST': #clicked on 'Proceed to Pay'
		return redirect('payment-home')
		# is_prepared = order_obj.is_done()
		# if is_prepared:
		# 	did_charge,msg = billing_profile.charge(order_obj)
		# 	if did_charge:
		# 		order_obj.mark_paid()	#mark the Order as Paid
		# 		del request.session['booking_id'] #delete the Booking from session
		# 		return redirect('bookings:success') #make this 'billing:success'
		# 	else:
		# 		return redirect('bookings:home')
			# associate the order to user's order history
	context={
		'order_obj':order_obj,
		'billing_profile':billing_profile,
		'login_form':login_form,
	}
	return render(request,'bookings/checkout.html',context)


def payment_home(request,*args,**kwargs):
	billing_profile,created = BillingProfile.objects.new_or_get(request)
	booking_obj,created = Booking.objects.new_or_get(request)
	order_obj,created = Order.objects.new_or_get(billing_profile,booking_obj)
	has_card = billing_profile.has_card
	if request.method == 'POST': #clicked on 'Confirm Payment'
		is_prepared = order_obj.is_done()
		if is_prepared:
			did_charge,msg = billing_profile.charge(order_obj)
			if did_charge:
				order_obj.mark_paid()	#mark the Order as Paid
				del request.session['booking_id'] #delete the Booking from session
				return redirect('bookings:success') #make this 'billing:success'
			else:
				return redirect('bookings:home')
	context={
		'has_card':has_card,
		'order_obj':order_obj,
		'billing_profile':billing_profile,
		'publish_key':STRIPE_PUB_KEY,
	}
	return render(request,'bookings/paymenthome.html',context)


def checkout_success(request,*args,**kwa):
	#attach the order details to user profile
	return render(request,'bookings/success.html',{})


