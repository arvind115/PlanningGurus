from django.contrib import admin

from .models import Booking,Detail

class BookingAdmin(admin.ModelAdmin):
	list_display=['date_added','booking_date','__str__','event','emf','city','user']
	class Meta:
		model = Booking
	def amount_(self,obj):
		if obj.amount.amount:
			return obj.amount.amount
admin.site.register(Booking,BookingAdmin)

admin.site.register(Detail)