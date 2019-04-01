from django.db import models
from django.db.models.signals import pre_save,post_save
from django.utils.text  import slugify

from events.models import Event
# Create your models here.
class EmfManager(models.Manager):
	def get_by_id(self,id):
		qs = self.get_queryset().filter(id=id)
		if qs.count() == 1:
			return qs.first()
		else:
			return None

class Emf(models.Model):
	EVENT_CHOICES 	= (
			('birthday','Birthday'),
			('wedding','Wedding'),
			('dwedding','DWedding'),
			('anniversary','Anniversary'),
			('festive','Festive'),
			('special','Special'),
			('corporate','Corporate'),
		)
	title 		= models.CharField(max_length=60,blank=False,unique=True) #name of the firm
	slug		= models.SlugField(default='abcd')
	# city 		= models.CharField(max_length=50,blank=False) 	#main city of operation
	region 		= models.CharField(max_length=50)				#region of operation 
	email 		= models.EmailField(blank=True,					#email
									unique=True,
									max_length=50)
	phone 		= models.CharField(max_length=12,blank=False,unique=True,) #phone no (to be changed later) 
	events 		= models.ManyToManyField(Event,blank=True)

	objects 	= EmfManager()  #objects = QuerySet()

	def __str__(self):
		return self.title

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return "/emfs/{slug}".format(slug=self.slug)

def emf_pre_save_reciever(sender,instance, *args, **kwargs):
	instance.slug = slugify(instance.title)

pre_save.connect(emf_pre_save_reciever,sender=Emf)
