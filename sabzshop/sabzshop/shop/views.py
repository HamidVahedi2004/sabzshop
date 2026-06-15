from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import *
from cart.cart import Cart
# Create your views here.


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()

    # فیلتر دسته‌بندی
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # فیلتر جنسیت
    gender = request.GET.get("gender")
    if gender in ['مردانه', 'زنانه']:
        products = products.filter(description__icontains=gender)

    # فیلتر موجودی
    available = request.GET.get("available")
    if available == "1":
        products = products.filter(inventory__gt=0)

    context = {
        'category': category,
        'categoryes': categories,
        'products': products,
    }
    return render(request, 'shop/list.html', context)



def product_detail(request, id, slug):
    product= get_object_or_404(Product, id=id, slug=slug)
    if 'مردانه' in product.description:
        gender_word= 'مردانه'
    elif 'زنانه' in product.description:
        gender_word= 'زنانه'
    else:
        gender_word= None
        
    if gender_word:
        similar_post= Product.objects.filter(description__icontains=gender_word).exclude(id=product.id)[:4]
    else:
        similar_post = Product.objects.none
    phone= request.session.get('phone')
    return render(request, 'shop/detail.html', {'product':product, 'phone':phone, 'similar_post':similar_post,})



def product_filtering(request):
    product= Product.objects.all()
    
    # فیلتر حنسیت
    gender= request.GET.get("gender")
    if gender in ['مردانه', 'زنانه']:
        products= product.filter(description__icontains= gender)
        
    # فیلتر موجودی
    available= request.GET.get("available")
    if available == "1":
        products= product.filter(inventory__gt= 0)
    
   