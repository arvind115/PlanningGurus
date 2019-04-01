from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save,post_save
from django.urls import reverse

import stripe
stripe.api_key = 'sk_test_jcscEC3iRnTzBfAU7jfVf61o00d4ZW7mqH'
User = settings.AUTH_USER_MODEL

class BillingManager(models.Manager):
    def new_or_get(self,request):
        '''
        If the User is_authenticated,he/she MUST have a BillingProfile associated.
        Else the user hasn't logged in yet.So, return a None object
        '''
        user,obj,created = request.user,None,False
        if user.is_authenticated: #user has both username & email
            obj,created = self.get_or_create(user=user,email=user.email)
        return obj,created

    def get_or_create(self,user=None,email=None):
        oj,created = None,False
        if email is not None and user is not None:
            qs = self.get_queryset().filter(email=email)
            if qs.exists(): #already a profile.
                obj,created = qs.first(),False
            else: #need to create NEW BillingProfile
                obj = self.model.objects.create(user=user,email=email)
                created = True
                print('\n\n BillingProfile created for ',user,'\n\n')
        return obj,created

class BillingProfile(models.Model):
    user    = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    email   = models.EmailField(null=True,blank=True)
    active  = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    customer_id = models.CharField(max_length=120,null=True,blank=True)

    objects = BillingManager()

    def __str__(self):
        return self.email

    def charge(self, order_obj, card = None):
        return Charge.objects.do(self, order_obj, card)

    def get_cards(self):
        return self.card_set.all()

    def get_payment_method_url(self):
        return reverse('payment-method')

    @property
    def has_card(self): # instance.has_card
        card_qs = self.get_cards()
        return card_qs.exists() # True or False

    @property
    def default_card(self):
        default_cards = self.get_cards().filter(active=True, default=True)
        if default_cards.exists():
            return default_cards.first()
        return None

    def set_cards_inactive(self):
        cards_qs = self.get_cards()
        cards_qs.update(active=False)
        return cards_qs.filter(active=True).count()

def billing_profile_created_reciever(sender,instance,*args,**kwargs):
    if not instance.customer_id and instance.email:
        customer = stripe.Customer.create(email = instance.email)
        instance.customer_id = customer.id

pre_save.connect(billing_profile_created_reciever,sender=BillingProfile)

def user_created_reciever(sender,instance,created,*args,**kwargs):
    '''A BillingProfile gets created for every new User as soon as he/she registers.'''
    if created: #user has just been created
        BillingProfile.objects.get_or_create(user=instance,email=instance.email)
post_save.connect(user_created_reciever,sender=User)


class CardManager(models.Manager):
    def all(self, *args, **kwargs): # ModelKlass.objects.all() --> ModelKlass.objects.filter(active=True)
        return self.get_queryset().filter(active=True)

    def add_new(self, billing_profile, token):
        if token:
            customer = stripe.Customer.retrieve(billing_profile.customer_id)
            stripe_card_response = customer.sources.create(source=token)
            new_card = self.model(
                    billing_profile=billing_profile,
                    stripe_id = stripe_card_response.id,
                    brand = stripe_card_response.brand,
                    country = stripe_card_response.country,
                    exp_month = stripe_card_response.exp_month,
                    exp_year = stripe_card_response.exp_year,
                    last4 = stripe_card_response.last4
                )
            new_card.save()
            return new_card
        return None


class Card(models.Model):
    billing_profile         = models.ForeignKey(BillingProfile,on_delete=models.CASCADE)
    stripe_id               = models.CharField(max_length=120) #stripe_customer_id
    brand                   = models.CharField(max_length=120, null=True, blank=True)
    country                 = models.CharField(max_length=20, null=True, blank=True)
    exp_month               = models.IntegerField(null=True, blank=True)
    exp_year                = models.IntegerField(null=True, blank=True)
    last4                   = models.CharField(max_length=4, null=True, blank=True)
    default                 = models.BooleanField(default=True)
    active                  = models.BooleanField(default=True)
    timestamp               = models.DateTimeField(auto_now_add=True)

    objects = CardManager()

    def __str__(self):
        return "{} {}".format(self.brand, self.last4)


def new_card_post_save_receiver(sender, instance, created, *args, **kwargs):
    if instance.default:
        billing_profile = instance.billing_profile
        qs = Card.objects.filter(billing_profile=billing_profile).exclude(pk=instance.pk)
        qs.update(default=False)
        #mark the rest of the cards as 'inactive'

post_save.connect(new_card_post_save_receiver, sender=Card)


class ChargeManager(models.Manager):
    def do(self, billing_profile, order_obj, card=None): # Charge.objects.do()
        card_obj = card
        if card_obj is None:
            cards = billing_profile.card_set.filter(default=True) # card_obj.billing_profile
            if cards.exists():
                card_obj = cards.first()
        if card_obj is None:
            return False, "No cards available"
        c = stripe.Charge.create(
              amount = int(order_obj.booking.amount.amount * 100), # 39.19 --> 3919
              currency = "usd",
              customer =  billing_profile.customer_id,
              source = card_obj.stripe_id,
              metadata={"order_id":order_obj.order_id},
            )
        new_charge_obj = self.model(
                billing_profile = billing_profile,
                stripe_id = c.id,
                paid = c.paid,
                refunded = c.refunded,
                outcome = c.outcome,
                outcome_type = c.outcome['type'],
                seller_message = c.outcome.get('seller_message'),
                risk_level = c.outcome.get('risk_level'),
        )
        new_charge_obj.save()
        return new_charge_obj.paid, new_charge_obj.seller_message


class Charge(models.Model):
    billing_profile         = models.ForeignKey(BillingProfile,on_delete=models.CASCADE)
    stripe_id               = models.CharField(max_length=120)
    paid                    = models.BooleanField(default=False)
    refunded                = models.BooleanField(default=False)
    outcome                 = models.TextField(null=True, blank=True)
    outcome_type            = models.CharField(max_length=120, null=True, blank=True)
    seller_message          = models.CharField(max_length=120, null=True, blank=True)
    risk_level              = models.CharField(max_length=120, null=True, blank=True)

    objects = ChargeManager()
