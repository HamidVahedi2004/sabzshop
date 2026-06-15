from . import views
from django.urls import path

app_name="order"

urlpatterns = [
    path('verify-phone', views.verify_phone, name="verify_phone"),
    path('verify-code', views.verify_code, name="verify_code"),
    path('order-create', views.order_create, name="order_create"),
    path('pay/', views.send_payment_request, name='pay'),
    path('verify/', views.verify_payment, name='verify'),
    path('order_list/', views.order_list, name='order_list'),
    path('order_detail/<int:id>', views.order_detail, name='order_detail'),
]