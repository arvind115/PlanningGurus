from django.db import models

# Create your models here.
class User(models.Model):
	name 	= models.CharField(max_length=120)
	email 	= models.TextField()
	phone 	= models.TextField()
	address = models.TextField()
