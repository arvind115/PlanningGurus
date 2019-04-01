from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import Http404
from .models import Event
from bookings.models import Booking


class EventDetailSlugView(DetailView):
	# queryset = Event.objects.all() #won't work here as we need a single object
	template_name = "events/event.html"

	def get_object(self):
		request = self.request
		slug = self.kwargs.get('slug')
		instance = Event.objects.get_by_slug(slug=slug) #get_object_or_404 = (Event, slug = slug)
		if instance is None:
			raise Http404("Event not found ")
		return instance
	def get_context_data(self,*args,**kwargs):
		context = super(EventDetailSlugView,self).get_context_data(*args,**kwargs)
		event = self.get_object() #get the required event
		# providers = event.emf_set.all() delete this line. has been done in the html file itself
		# context['providers']=providers #service providers for the event
		context['event']=event
		booking_obj, created = Booking.objects.new_or_get(self.request)
		context['booking_obj'] = booking_obj
		return context

class EventListView(ListView):
	queryset = Event.objects.all()
	template_name = "events/eventlist.html"

	def get_context_data(self,*args,**kwargs):
		context = super(EventListView,self).get_context_data(*args,**kwargs)
		print(context)
		eventlist = Event.objects.all()
		context['eventlist'] = eventlist
		return context
