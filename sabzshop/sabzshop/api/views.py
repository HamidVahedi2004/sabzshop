from django.shortcuts import render
from shop.models import Product
from .serializers import ProductSerializer, ShopUserSerializer, UserRegistrationSerializer, OrderSerializer
from order.models import Order
from rest_framework import generics
from rest_framework import views
from account.models import ShopUser
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from rest_framework import viewsets
from rest_framework.decorators import action
from .permissions import IsAdminTehran, IsBuyer
# Create your views here.


# class ProductListApiView(generics.ListAPIView):
#     queryset= Product.objects.all()
#     serializer_class= ProductSerializer
    
    
# class ProductDetailApiView(generics.RetrieveAPIView):
#     queryset= Product.objects.all()
#     serializer_class= ProductSerializer
    
    
class UserListApiView(views.APIView):
    authentication_classes=[BasicAuthentication]
    permission_classes= [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        users= ShopUser.objects.all()
        serializer= ShopUserSerializer(users, many=True)
        return Response(serializer.data)
    
    
class UserRegistrationApiView(generics.CreateAPIView):
    permission_classes= [AllowAny]
    queryset= ShopUser.objects.all()
    serializer_class= UserRegistrationSerializer
    
    
class ProductViewSet(viewsets.ModelViewSet):
    queryset= Product.objects.all()
    serializer_class= ProductSerializer
    
    
    @action(detail=False, methods=['GET'], url_path='all_discount_products', url_name='all_discount_products', permission_classes= [AllowAny])
    def discount_products(self, request):
        min_discount= request.query_params.get('min_discount')
        try:
            min_discount= int(min_discount)
        except ValueError:
            return Response({'errors': 'value error for min_discount'})
        products= self.queryset.filter(off__gt=min_discount)
        serializer= self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    
        
class OrderListApiView(generics.ListAPIView):
    queryset= Order.objects.all()
    serializer_class= OrderSerializer
    permission_classes=[IsAdminTehran]
    
    

class  OrderDetailApiView(generics.RetrieveAPIView):
    queryset= Order.objects.all()
    serializer_class= OrderSerializer
    permission_classes=[IsBuyer]

    