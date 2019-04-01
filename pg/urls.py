"""pg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from .views import home_view,blog_view,contact_view,coming_soon, index_view
from billing.views import payment_method_view, payment_method_create_view
from marketing.views import MarketingPreferenceUpdateView, MailchimpWebhookView

from bookings.views import payment_home

urlpatterns = [
	path('',home_view,name='home'),
    path('admin/', admin.site.urls),
    path('contact/',contact_view,name='contact'),
    path('blog/',blog_view,name='blog'),
    
    path('billing/payment-method/',payment_method_view,name='payment-method'),
    path('billing/payment-method/create/',payment_method_create_view,name='payment-method-endpoint'),
    path('payment/',payment_home,name='payment-home'),

    path('accounts/',include('accounts.urls',   namespace='accounts')),

    path('event/',   include('events.urls',     namespace='events')),   
    
    path('emfs/',    include('emfs.urls',       namespace='emfs')),
    
    path('bookings/',include('bookings.urls',   namespace='bookings')),
    
    path('search/',  include('search.urls',     namespace='search')),

    # path('bookings&event=<slug:event>',new_view,name='new'),
    path('settings/email/', MarketingPreferenceUpdateView.as_view(), name='marketing-pref'),
    path('webhooks/mailchimp/', MailchimpWebhookView.as_view(), name='webhooks-mailchimp'),


    path('index', index_view, name = 'index'),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)