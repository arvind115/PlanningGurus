from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView

from emfs.models import Emf
from bookings.models import Booking
from bookings.forms import BookingForm

class SearchEmfView(ListView):
	template_name = "bookings/booking.html" #this helps us keep the 'BookingForm'

	def get_context_data(self,*args,**kwargs):
		context = super(SearchEmfView,self).get_context_data(*args,**kwargs)
		request=self.request
		booking_obj,created = Booking.objects.new_or_get(request)
		# data = {'city':booking_obj.city,'event':booking_obj.event}
		context['form'] = BookingForm()
		context['booking_obj'] = booking_obj
		context['queryset'],context['found'] = self.get_queryset(args,kwargs)
		return context

	def get_queryset(self,*args,**kwargs): #do all the search logic here
		request = self.request
		query = request.GET.get('q',None)
		if query is not None: #if there is a city, consider updating city.
			print('Q:: ',query.split())
			qs = Emf.objects.none()
			print('INITIAL []',qs)
			for word in query.split():
				if word in ['in','at','on','here','near','under','upon']: #bogus words
					continue
				lookups = ( Q(city__city__icontains=word)|
							Q(events__event__icontains=word)| 
							Q(title__icontains=word)
							)
				qs = qs | Emf.objects.filter(lookups).distinct()
				print('Search tag: ',word,'QS::',qs)
			if qs.count():
				return qs.distinct(),True
			return Emf.objects.none(),False #else
		return Emf.objects.none(),False