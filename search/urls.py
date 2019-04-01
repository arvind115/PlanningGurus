from django.urls import path

from .views import SearchEmfView

app_name = 'search'
urlpatterns = [
	path('',SearchEmfView.as_view(),name='query'), #rendered for 127.0.0.1:8000/search
]