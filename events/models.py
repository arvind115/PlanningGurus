from django.db import models
from django.db.models.signals import pre_save,post_save
from django.utils.text import slugify
from django.urls import reverse
# Create your models here.

class EventManager(models.Manager):
	def get_by_id(self,pk):
		qs = self.get_queryset().filter(pk=pk)
		if qs.count() == 1:
			return qs.first()
		return None
	def get_by_slug(self,slug):
		qs = self.get_queryset().filter(slug=slug)
		if qs.count() == 1:
			return qs.first()
		return None

class Event(models.Model):
	event 		= models.CharField(max_length=50,null=True,blank=True)
	slug 		= models.SlugField(default='abc')
	description = models.CharField(max_length=1500,null=True,blank=True)
	image 		= models.FileField(upload_to='event/',null=True,blank=True)
	#video add a video field here

	objects = EventManager()

	# def save(self,*args,**kwargs):
	# 	self.slug = slugify(self.event)  #create a slug field
	# 	super(Event,self).save(*args,*kwargs)

	def __str__(self):
		return self.event
	
	def get_absolute_url(self):
		# return "/event/{slug}".format(slug=self.slug)
		return reverse("event:eventDSView", kwargs={'slug':self.slug})

def event_pre_save_reciever(sender, instance, *args, **kwargs):
	instance.slug = slugify(instance.event)
	print(instance.slug)

pre_save.connect(event_pre_save_reciever,sender=Event)