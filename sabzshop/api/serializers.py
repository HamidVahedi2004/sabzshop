from rest_framework import serializers
from shop.models import Product, Productfeature
from account.models import ShopUser
from order.models import Order


class ProductFeatureSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= Productfeature
        fields= ['name', 'value']



class ProductSerializer(serializers.ModelSerializer):
    
    feature= ProductFeatureSerializer(many=True, read_only=True)
    class Meta:
        model= Product
        fields= ['id', 'name', 'new_price', 'feature']
        

        
class ShopUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= ShopUser
        fields= ['id', 'first_name', 'last_name', 'address', 'is_staff', 'is_active', 'date_join']
        
        

class  UserRegistrationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= ShopUser
        fields= ['phone', 'first_name', 'last_name', 'address', 'password']
        extra_kwargs= {'password':{'write_only':True}}
    
    
    def create(self, validated_data):
        user= ShopUser(phone=validated_data['phone'], 
                       first_name=validated_data['first_name'],
                       last_name=validated_data['last_name'],
                       address=validated_data['address'],
                       password=validated_data['password'],
                       )
        
        user.set_password= validated_data['password']
        user.save()
        return user
    
    
class OrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= Order
        fields= '__all__'