from django.contrib import admin

from .models import Order

class OrderAdmin(admin.ModelAdmin):
	list_display=['__str__','status','Booking_ID','booking_','date','total']
	class Meta:
		model = Order 
	def total(self,obj):
		return obj.booking.amount.amount
	def Booking_ID(self,obj):
		return obj.booking.id
	def booking_(self,obj):
		return obj.booking.event.event +'-'+ obj.booking.city.city + '-' + obj.booking.emf.title
	def date(self,obj):
		return obj.booking.booking_date
admin.site.register(Order,OrderAdmin)