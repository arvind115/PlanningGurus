from django.contrib import admin

# Register your models here.

from .models import City

class CityAdmin(admin.ModelAdmin):
	list_display = ['city','id','emfs_in_city']
	class Meta:
		model = City
	def emfs_in_city(self,obj):
		return [x for x in obj.emf.all()]


admin.site.register(City,CityAdmin)