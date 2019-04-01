from django.contrib import admin

from .models  import Price

class PriceAdmin(admin.ModelAdmin):
	list_display=['__str__','amount']
	class Meta:
		model = Price

admin.site.register(Price,PriceAdmin)