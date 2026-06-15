from django.db import models
from shop.models import Product
from account.models import ShopUser
from cart.common.kavenegar import send_sms
# Create your models here.
import kavenegar
from kavenegar import KavenegarAPI, APIException, HTTPException


class Order(models.Model):
    
    class Status(models.TextChoices):
        Pending_Review= 'PR', 'pending review'
        Order_Confirmed= 'oc', 'order confirmed'
        Recevied_From_Seller= 'RFS', 'received from seller'
        Preparing_Order= 'PO', 'preparing order'
        Deliverd_To_Postal_Service= 'DTPS', 'deliverd to postal service'
        Refunded_Due_To_Out_Of_Stock= 'RDTOOS', 'refunded due to out of stock'    
    
    buyer= models.ForeignKey(ShopUser, related_name="orders", on_delete=models.SET_NULL, null=True, blank=True)
    firstname= models.CharField(max_length=100)
    lastname= models.CharField(max_length=100)
    phone= models.CharField(max_length=11)
    address= models.CharField(max_length=255)
    postal_code= models.CharField(max_length=11)
    province= models.CharField(max_length=255)
    city= models.CharField(max_length=255)
    created= models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now=True)
    paid= models.BooleanField(default=False)
    status= models.CharField(choices=Status.choices, default=Status.Pending_Review)
    
    
    class Meta:
        ordering= ['-created']
        indexes= [
            models.Index(fields=['-created']),
        ]
        
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    
    
    def get_post_cost(self):
        weight= sum(item.get_weight() for item in self.items.all())
        if weight <= 1000:
            return 82000
        elif 1000 < weight < 3000:
            return 100000
        else:
            return 172000
        
        
    def get_finel_cost(self):
        price= self.get_total_cost() + self.get_post_cost()
        return price
        
        
    def __str__(self):
        return f"order{self.id}"
    
    
                

class Orderitem(models.Model):
    order= models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product= models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    price= models.PositiveBigIntegerField(default=0)
    quantity= models.PositiveBigIntegerField(default=1)
    weight= models.PositiveBigIntegerField(default=0)
    
    
    def get_cost(self):
        return self.price * self.quantity
    
    def get_weight(self):
        weight= self.weight * self.quantity
        return weight
    
    def __str__(self):
        return f"order item{self.id}"
    
    
    

class Transaction(models.Model):
    STATUS_CHOICES= (
        ('pending', 'pending'),
        ('success', 'success'),
        ('failed', 'failed')
    )
    order= models.ForeignKey(Order, related_name='transaction', on_delete=models.CASCADE)
    price= models.DecimalField(max_digits=10, decimal_places=2)
    status= models.CharField(choices= STATUS_CHOICES, default='pending')
    buy_time= models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f'Transaction {self.id} -- {self.status}'