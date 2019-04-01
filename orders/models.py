from django.db import models

from django.db.models.signals import pre_save,post_save
from pg.utils import unique_order_id_generator

from bookings.models import Booking
from billing.models import BillingProfile

ORDER_CHOICES=(
	('created','Created'),
	('paid','Paid'),
	('done','Done'), #event happened
	('refunded','Refunded')
	)

class OrderManager(models.Manager):
	#an order is ONLY created when we have both a BillingProfile & a Booking object
	def new_or_get(self,billing_profile,booking_obj):
		created = False
		qs = self.get_queryset().filter(
				billing_profile=billing_profile,
				booking = booking_obj,
				active=True).exclude(status='paid')
		if qs.count() == 1:
			obj = qs.first()
		else: #need to create a new Order object for current billing_profile & booking_obj
			obj = self.model.objects.create(
					billing_profile=billing_profile,
					booking=booking_obj)
			created = True
		if created:
			print('Order created ',obj)
		return obj,created

class Order(models.Model):
	order_id 		= models.CharField(max_length=6,null=True,blank=True) #has to be RANDOM & UNIQUE
	status			= models.CharField(max_length=30,null=True,blank=True,choices=ORDER_CHOICES,default='created')
	booking 		= models.ForeignKey(Booking,on_delete=models.CASCADE)
	billing_profile = models.ForeignKey(BillingProfile,on_delete=models.CASCADE,null=True)
	active 			= models.BooleanField(default=True)

	objects = OrderManager()

	def __str__(self):
		return self.order_id

	def is_done(self):
		booking 		= self.booking #Order has a booking attached 
		billing_profile = self.billing_profile #Order has a BillingProfile attached
		if booking and billing_profile:
			return True
		return False

	def mark_paid(self):
		if self.is_done():
			self.status='paid'
			self.active = False
			self.save()
		return self.status

 
	def get_absolute_url(self):
		# return "/event/{slug}".format(slug=self.slug)
		return reverse("bookings:checkout", kwargs={'order_id':self.order_id})
		#the above usl isn't functional. make changes in bookings.urls.py

def unique_order_id_pre_save_reciever(sender,instance,*args,**kwargs):
	if instance.order_id is None: #created for the first time, need a random ID
		instance.order_id = unique_order_id_generator(instance)
	#find the Orders with same booking objects, & make them inactive
	qs = Order.objects.filter(booking=instance.booking).exclude(billing_profile=instance.billing_profile)
	if qs.exists():
		qs.update(active=False)

pre_save.connect(unique_order_id_pre_save_reciever,sender=Order)
