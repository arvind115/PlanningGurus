from django.contrib import admin

# Register your models here.
from .models import Emf


class EmfAdmin(admin.ModelAdmin):
	list_display= ['__str__','slug','email','eve','cities']
	class Meta:
		model = Emf
	def eve(self,obj):
		return [x.event for x in obj.events.all()]
	def cities(self,obj):
		return [x for x in obj.city_set.all()]

admin.site.register(Emf,EmfAdmin)