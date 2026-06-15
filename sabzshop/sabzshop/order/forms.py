from django import forms
from .models import *


class PhoneVerificationForm(forms.Form):
    phone= forms.CharField(max_length=11, label="شماره تلفن")
    
    def clean_phone(self):
        phone= self.cleaned_data["phone"]
        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError("تلفن همراه بایستی عدد باشد")
            elif len(phone) != 11:
                raise forms.ValidationError("تعداد اعداد بیش از حد مجاز میباشد")
            elif not phone.startswith("09"):
                raise forms.ValidationError("فرمت تلفن همراه شما اشتباه هست")
            else:
                return phone
            
            
            
class OrderCreateForm(forms.ModelForm):
    class Meta:
        model= Order
        fields=['firstname', 'lastname', 'phone', 'address', 'postal_code', 'province', 'city']
        