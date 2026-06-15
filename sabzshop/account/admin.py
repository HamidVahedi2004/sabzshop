from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .forms import ShopUserChangeForm, ShopUserCreationForm


# Register your models here.
@admin.register(ShopUser)
class UserAdmin(UserAdmin):
    ordering= ['phone']
    list_display = ['phone', 'first_name', 'last_name', 'is_staff', 'is_active']
    add_form= ShopUserCreationForm
    form= ShopUserChangeForm
    model= ShopUser
    fieldsets = (
        ('None', {'fields':('phone', 'password')}),
        ('Personal Info', {'fields':('first_name', 'last_name', 'address')}),
        ('Premissions', {'fields':('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Importent dates', {'fields':('last_login', 'date_join')}),
    )
    
    add_fieldsets = (
        ('None', {'fields':('phone', 'password1', 'password2')}),
        ('Personal Info', {'fields':('first_name', 'last_name', 'address')}),
        ('Premissions', {'fields':('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Importent dates', {'fields':('last_login', 'date_join')}),
    )