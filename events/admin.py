from django.contrib import admin

from .models import Event
# Register your models here.

class EventAdmin(admin.ModelAdmin):
	list_display= ['__str__','slug','EMF','image']
	class Meta:
		model = Event
	def EMF(self,obj):
		return [x for x in obj.emf_set.all()]
admin.site.register(Event,EventAdmin)