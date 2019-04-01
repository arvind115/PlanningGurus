from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from django.http import Http404

from .models import Emf
from bookings.models import Booking

class EmfListView(ListView):
	template_name = 'emfs/emflist.html' 
	
	def get_context_data(self,*args,**kwargs):
		context = super(EmfListView,self).get_context_data(*args,**kwargs)
		context['emfs'] = Emf.objects.all()
		booking_obj, created = Booking.objects.new_or_get(self.request)
		context['booking_obj'] = booking_obj
		return context

	def get_queryset(self,*args,**kwargs): #overriding the 'get_queryset()' method
		return Emf.objects.all()

class EmfDetailSlugView(DetailView):
	template_name = 'emfs/emfdetail.html'

	def get_context_data(self,*args,**kwargs):
		context = super(EmfDetailSlugView,self).get_context_data(*args,**kwargs)
		booking_obj, created = Booking.objects.new_or_get(self.request)
		context['booking_obj'] = booking_obj
		return context	

	def get_object(self,*args,**kwargs): #overriding the 'get_object()' method
		request 	= self.request
		slug 		= self.kwargs.get('slug')
		instance 	= get_object_or_404(Emf,slug=slug)
		if instance is None:
			raise Http404("Emf doesn't exist")
		return instance