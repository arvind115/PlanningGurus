from django.urls import path,re_path

from .views import (
	login_view,
	RegisterView,
	logout_view,
	)

app_name = 'accounts'

urlpatterns = [
	path('login/',login_view,name='login'),
	path('logout/',logout_view,name='logout'),
	path('register/',RegisterView.as_view(),name='register'),
]