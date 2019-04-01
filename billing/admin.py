from django.contrib import admin

# Register your models here.
from .models import BillingProfile, Card, Charge

class BillingProfileAdmin(admin.ModelAdmin):
	list_display = ['email']
	class Meta:
		model= BillingProfile
	# def username(self,obj): #the obj is the object of 'BillingProfile', self is the object of 'BillingProfileAdmin'
	# 	if obj.user.name:
	# 		return obj.user.name
	# 	return None

admin.site.register(BillingProfile,BillingProfileAdmin)

admin.site.register(Card)

admin.site.register(Charge)