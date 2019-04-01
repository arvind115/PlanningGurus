from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save,post_save

from datetime import datetime

from events.models import Event
from cities.models import City
from emfs.models import Emf
from pricing.models import Price

User = settings.AUTH_USER_MODEL


DECOR_CHOICES = (
	('floral','Floral'),
	('sober','Sober'),
	('premium','Premium'),
	('artificial','Artificial'),
	)

class Detail(models.Model):
	decor 				= models.CharField(max_length=40,choices=DECOR_CHOICES,null=True,blank=True)
	photography 		= models.BooleanField(default=True)
	people 				= models.IntegerField()
	DJ_Entertainment	= models.BooleanField(default=False) 


class BookingManager(models.Manager):
	def new_or_get(self,request):
		'''
		A Booking object stays in the session dict as long as the user doesn't log out.
		One session ---> one Booking object
		'''
		booking_id = request.session.get('booking_id',None)
		qs = self.get_queryset().filter(id=booking_id)
		if qs.count() == 1: #already exists
			booking_obj, created = qs.first() , False# print('Booking EXISTS')
			if booking_obj.user is None and request.user.is_authenticated:
				booking_obj.user = request.user
				booking_obj.save()
		else:
			booking_obj,created = Booking.objects.new(user=request.user),True
			request.session['booking_id'] = booking_obj.id
		return booking_obj, created

	def new(self,user=None): #helper method for above method
		user_obj = None
		if user is not None:
			if user.is_authenticated:
				user_obj = user
		return self.model.objects.create(user=user_obj)

class Booking(models.Model):
	user 			= models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
	date_added		= models.DateTimeField(auto_now_add=True,null=True,blank=True)	 
	booking_date 	= models.DateField(null=True,blank=True)
	city 			= models.ForeignKey(City,on_delete=models.CASCADE,null=True,blank=True)
	event 			= models.ForeignKey(Event,on_delete=models.CASCADE,null=True,blank=True)
	emf 			= models.ForeignKey(Emf,on_delete=models.CASCADE,null=True,blank=True)
	amount	 		= models.ForeignKey(Price,on_delete=models.CASCADE,null=True,blank=True) #the emf charge
	details 		= models.ForeignKey(Detail,on_delete=models.CASCADE,null=True,blank=True)

	objects = BookingManager()

	def __str__(self):
		return str(self.id)

def booking_date_pre_save_reciever(sender,instance,*args,**kwargs):
	instance.date_added = datetime.today() #assigns the current date

# pre_save.connect(booking_date_pre_save_reciever,sender=Booking) #there was some runtime error of naive
#date time field

def pre_save_find_price_reciever(sender,instance,*args,**kwargs):
	'''
	A Booking object is associated with an appropriate Price object before saving.If a relevant Price 
	object exists. Else no changes are made. (an invalid choice was made )
	'''
	print('\n\tBefor saving Booking\n')
	if instance.event and instance.emf: #if both have been selected.
		print("Calculating Total for Booking",instance.id)
		print('EVENT: ',instance.event,'   EMF: ',instance.emf)
		lookups = (Q(event__event__iexact=instance.event)&
					Q(emf__title__iexact=instance.emf)
					)
		qs = Price.objects.filter(lookups) #check if a price object exists or not
		if qs.count() == 1: #we have a Price object
			print('We have a price object')
			instance.amount = qs.first() #link to the price object
		else:
			print('\n\tNO price object for ',instance.event,' and ',instance.emf,'\n')
	else:
		print("\nbooking object isn't complete yet\n")
pre_save.connect(pre_save_find_price_reciever,sender=Booking)
