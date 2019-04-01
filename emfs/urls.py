from django.urls import path,re_path

from .views import (
	EmfListView,
	EmfDetailSlugView,
	)

app_name = 'emfs'

urlpatterns = [
	path('',EmfListView.as_view(),name='emfs'),
	# path('<slug:emf>',EmfDetailSlugView.as_view(),name='emfsd'), #why this doesn't work ???
    re_path(r'^(?P<slug>[\w-]+)/$',EmfDetailSlugView.as_view(),name='emfsd'),

]