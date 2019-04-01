import random
import string

from django.utils.text import slugify

def random_string_generator(size=6,chars=string.ascii_uppercase+string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def unique_order_id_generator(instance):
	new_order_id = random_string_generator(size=6)
	Kclass = instance.__class__
	qs_exists = Kclass.objects.filter(order_id=new_order_id).exists()
	if qs_exists:
		return unique_order_id_generator(instance)
	return new_order_id