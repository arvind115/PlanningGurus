from django.urls import path, re_path

from .views import (
	 EventListView,
	 EventDetailSlugView,
	 )
app_name = 'event'
urlpatterns = [ 
	path('',EventListView.as_view(),name='event'),
    re_path(r'^(?P<slug>[\w-]+)/$',EventDetailSlugView.as_view(),name='eventDSView'),
]
