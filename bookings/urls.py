from django.urls import path,re_path

from .views import (
	booking_view,
	booking_home,
	booking_update,
	detail_view,
	checkout,
	checkout_success
	)

app_name = 'bookings'

urlpatterns = [
	path('',booking_view,name='booking'),
	path('event=<slug:event>',booking_view,name='booking'), #make one for city only, and  one for both city & event
	path('home',booking_home,name='home'),
	path('update',booking_update,name='update'),
	path('detals',detail_view,name='details'),
	path('checkout',checkout,name='checkout'),
	path('success',checkout_success,name='success'),
]