from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
from . import views


router= DefaultRouter()
router.register('products', views.ProductViewSet)


app_name="api"
urlpatterns = [
    # path('products/', views.ProductListApiView.as_view(), name="producs_List_api"),
    # path('product/<pk>', views.ProductDetailApiView.as_view(), name="product_Detail_api"),
    path('users/', views.UserListApiView.as_view(), name="users_list_api"),
    path('register/', views.UserRegistrationApiView.as_view(), name="user_register_api"),
    path('', include(router.urls)),
    path('orders/', views.OrderListApiView.as_view(), name="orders"),
    path('orders/<int:pk>', views.OrderDetailApiView.as_view(), name="orders"),
]