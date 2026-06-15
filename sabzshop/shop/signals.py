from django.db.models.signals import pre_save
from .models import *
from django.dispatch import receiver

@receiver(pre_save, sender=Product)
def calculate_newprice(sender, instance, **kwargs):
    instance.new_price = instance.price - instance.off