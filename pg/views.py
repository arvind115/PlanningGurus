from django.shortcuts import render,redirect
from django.http import HttpResponse
from django import forms
from django.contrib.auth import authenticate, login, logout, get_user_model 
from events.models import Event
from bookings.models import Booking

def home_view(request,*args,**kwargs): 
	booking_obj,created = Booking.objects.new_or_get(request)
	events = Event.objects.all()
	context={
		'title':'Planning Gurus',
		'events':events,
		'booking_obj':booking_obj
	}
	return render(request, "home.html", context)
 
def index_view(request,*args,**kwargs):
	return render(request,'index.html',{})

def logout_view(request,*args,**kwargs):
	logout(request)
	return redirect('home')

def blog_view(request,*args,**kwargs):
	return render(request,"blog.html",{})

def coming_soon(request,*args,**kwargs):
	return render(request,"coming_soon.html",{})

def contact_view(request,*args,**kwargs):
	return render(request,"contact.html",{})