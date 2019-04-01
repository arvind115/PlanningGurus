from django.db import models

from emfs.models import Emf 
from events.models import Event 

class Price(models.Model):
	amount 	= models.DecimalField(null=True,blank=True,decimal_places=3,max_digits=100,default=1000)
	emf 	= models.ForeignKey(Emf,on_delete=models.CASCADE)
	event 	= models.ForeignKey(Event,on_delete=models.CASCADE)

	def __str__(self):
		return str(self.id) +'-' + self.emf.title +'-'+self.event.event


'''
make the process of Price object generations automated. When an Emf adds/removes its services, changes should 
reflect here.
'''