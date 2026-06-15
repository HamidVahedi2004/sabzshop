from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Order
from kavenegar import KavenegarAPI, APIException, HTTPException



@receiver(pre_save, sender=Order)
def status_change(sender, instance, **kwargs):
    if not instance:
        return 'salam'
    try:
        old_instance= Order.objects.get(pk= instance.pk)
    except Order.DoesNotExist:
        return 'This Order Does Not Exist'
    
    if old_instance.status != instance.status:
        try:
            api = KavenegarAPI('6172777A596E3368396B355A6C4C55556C4233774B6E2B484E465276436B487064463343694A74594546343D')
            params = {
                'sender': '2000660110',#optional
                'receptor': '09361465280',#multiple mobile number, split by comma
                'message': f'وضعیت سفارش شما به {instance.status} تغییر یافت',
            } 
            response = api.sms_send(params)
            print(response)
        except APIException as e: 
            print(e)
        except HTTPException as e: 
            print(e)
