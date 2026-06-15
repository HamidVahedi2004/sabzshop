from django.contrib import admin
from .models import *
import openpyxl
from django.http import HttpResponse
import csv

# # Register your models here.


# # Actions
def export_to_csv(modeladmin, request, queryset):
    response= HttpResponse(
        content_type= 'text/csv'
    )
    response['Content-Disposition']= 'attachment; filename="orders.csv"'
    
    writer= csv.writer(response)
    writer.writerow(['ID', 'First Name', 'Last Name', 'Phone', 'Address',
        'Postal Code', 'Province', 'City', 'Created',
        'Updated', 'Paid'])
    
    
    for order in queryset:
        created = order.created.replace(tzinfo=None) if order.created else ""
        updated = order.updated.replace(tzinfo=None) if order.updated else ""
        writer.writerow(
            [order.id,
            order.firstname,
            order.lastname,
            order.phone,
            order.address,
            order.postal_code,
            order.province,
            order.city,
            created,
            updated,
            order.paid,
            ]) 
    return response





def export_to_excel(modeladmin, request, queryset):
    # نوع محتوای اکسل
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    # مهم: attachment; (نقطه‌ویرگول)
    response['Content-Disposition'] = 'attachment; filename="orders.xlsx"'

    # ساخت فایل اکسل
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Order'

    # هدر ستون‌ها
    columns = [
        'ID', 'First Name', 'Last Name', 'Phone', 'Address',
        'Postal Code', 'Province', 'City', 'Created',
        'Updated', 'Paid'
    ]
    ws.append(columns)

    # ردیف‌ها
    for order in queryset:
        created = order.created.replace(tzinfo=None) if order.created else ""
        updated = order.updated.replace(tzinfo=None) if order.updated else ""
        ws.append([
            order.id,
            order.firstname,
            order.lastname,
            order.phone,
            order.address,
            order.postal_code,
            order.province,
            order.city,
            created,
            updated,
            order.paid,
        ])

    wb.save(response)
    return response


export_to_excel.short_description = 'Export to Excel'
export_to_csv.short_description= 'Export to Csv' 



class OrderInline(admin.TabularInline):
    model= Orderitem
    extra= 0
    raw_id_fields= ['product']
    
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display= ['id','status', 'buyer','firstname', 'lastname', 'phone', 'address', 'postal_code', 'province', 'city', 'created', 'updated', 'paid']
    list_filter= ['created', 'updated', 'paid']
    inlines= [OrderInline]
    actions=[export_to_excel, export_to_csv]
    
    

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display= ['id', 'get_buyer', 'get_price', 'buy_time', 'status']
    

    def get_buyer(self, obj):
        return obj.order.buyer
    
    
    def get_price(self, obj):
        return obj.order.get_finel_cost()



    get_buyer.short_description = ' Buyer'
    get_price.short_description = 'Price'




# Actions





 




