from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name= models.CharField(max_length=255, verbose_name='نام دسته بندی')
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        ordering= ['-name']
        indexes= [
            models.Index(fields=['name']),
           
        ]
        verbose_name ="دسته بندی"
        verbose_name_plural = " دسته بندی ها"
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])
    


class Product(models.Model):
    category= models.ForeignKey(Category, on_delete=models.CASCADE,related_name='products', verbose_name='دسته بندی')
    name= models.CharField(max_length=100, verbose_name='نام')
    slug= models.SlugField(max_length=255, unique=True, verbose_name='اسلاگ')
    description= models.TextField(max_length=1200, verbose_name='توضیحات')
    inventory= models.PositiveIntegerField(verbose_name="موجودی")
    weight= models.PositiveIntegerField(default=0, verbose_name='وزن')
    price= models.PositiveIntegerField(verbose_name='قیمت')
    off= models.PositiveIntegerField(default=0,verbose_name='تخفیف')
    new_price= models.PositiveIntegerField(default=0,verbose_name='قیمت ئس از تخفیف')
    created= models.DateTimeField(auto_now_add=True, verbose_name='زمان ایحاد')
    updated= models.DateTimeField(auto_now=True, verbose_name='زمان بروزرسانی')
    # gender= models.CharField(max_length=20, choices=[('men', 'مردانه'),('women', 'زنانه'),])
    
    
    class Meta:
        ordering= ['-created']
        indexes= [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]
        verbose_name ="محصول"
        verbose_name_plural = " محصولات"
        
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.id, self.slug])
    


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="محصول")
    title = models.CharField(verbose_name="موضوع")
    image_field= models.ImageField(upload_to="image_of_product/", height_field=None, width_field=None, max_length=None)
    description = models.TextField(verbose_name="توضیحات")
    created = models.DateTimeField(verbose_name="ساخت", auto_now_add=True)
    
    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields= ['-created'])
        ]
        verbose_name = "عکس"
        verbose_name_plural = "عکس ها"
    
    def __str__(self):
        return self.title


    
class Productfeature(models.Model):
    name= models.CharField(max_length=255, verbose_name='نام')
    value= models.CharField(max_length=255, verbose_name='مثدار ویژگی')
    product= models.ForeignKey(Product, on_delete=models.CASCADE, related_name='feature', verbose_name='ویژگی ها')
    
    def __str__(self):
        return self.name + ":" + self.value