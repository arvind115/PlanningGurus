from django.db import models
from django.db.models.signals import pre_save,post_save

from emfs.models import Emf

class City(models.Model):
	city = models.CharField(max_length=150,null=True,blank=True)
	emf  = models.ManyToManyField(Emf)

	class Meta:
		verbose_name='Cities'
		verbose_name_plural = 'Cities'

	def __str__(self):
		return self.city