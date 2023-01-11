from datetime import datetime
from django.db import models
import math
from django.db.models import Sum
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
# Create your models here.

User = settings.AUTH_USER_MODEL

class CustomUser(AbstractUser):
   dob = models.DateField(auto_now=False, auto_now_add=False,null=True,blank=True)
   phone_no = models.IntegerField(null=True,blank=True)
   gender = models.CharField(max_length=50,null=True,blank=True)

PRODUCT_SIZES = [
   ("XS","XS"),
   ("S","S"),
   ("M","M"),
   ("L","L"),
   ("XL","XL"),
   ("2XL","2XL"),
   ("3XL","3XL"),
   ("4XL","4XL"),
]

RISE_CHOICE= [
      ('Mid Waist','Mid Waist'),
      ('Low Waist','Low Waist'),
      ('High Waist','High Waist'),
]

GENDER_CHOICES = [
   ("girls","girls"),
   ("boys","boys"),
   ("women","women"),
   ("men","men"),
]

Size_CHOICES = [
   ("S","S"),
   ("XS","XS"),
   ("M","M"),
   ("L","L"),
   ("XL","XL"),
   ("2XL","2XL"),
   ("3XL","3XL"),
   ("4XL","4XL"),
   ("Free Size","Free Size"),
]

def user_directory_path(instance,filename):  
    if instance.gender =="women":
      x = "women"
    elif instance.gender =="men":
      x = "men"
    elif instance.gender =="girls":
         x = "girls"
    else:
         x = "boys"
    return '{0}/{1}/{2}'.format(x,instance.category,filename)

class KidsAge(models.Model):
   age = models.CharField(max_length=255,unique=True)
   def __str__(self):
      return self.age

class Color(models.Model):
   color = models.CharField(max_length=50,unique=True)
   def __str__(self):
      return self.color

class Size(models.Model):
   sizes = models.CharField(choices=Size_CHOICES,max_length=255)
   price = models.IntegerField()
   mrp = models.IntegerField(default=0)
   discount = models.CharField(max_length=100,null=True,blank=True)
   discnt_cat = models.CharField(max_length=100,default="Below 10%")
   stock = models.IntegerField()
   def save(self, force_insert = False, force_update = True, using = False):
      self.discount = math.floor((self.mrp - self.price)/self.mrp * 100)
      ds = math.floor(self.discount/10)
      self.discnt_cat = "Below 10%" if ds < 1 else str(ds*10 )+ "% And Above"
      try:
         carted = self.size_cart.get(size=self.id)
         ecom = EcomCartItem.objects.filter(cart=carted.cart)
         carted.save()
         carted.cart.total_qty = ecom.aggregate(quantity=Sum('quantity'))['quantity']  
         carted.cart.total_amnt = ecom.aggregate(total_price=Sum('total_price'))['total_price']
         carted.cart.dlvry_chrg = ecom.aggregate(delivery=Sum('delivery'))['delivery']
         carted.cart.save()
      except (EcomCartItem.DoesNotExist,ValueError):
         carted = ecom = 0
      return super().save()
   def __str__(self):
      #str(self.sizecharts.all()[0])+
      return "("+ str(self.discount) +")" +" ("+str(self.sizes) +")"
   
class Brand(models.Model):
   brand = models.CharField(max_length=255,unique=True)
   about = models.TextField(null=True,blank=True)
   def __str__(self):
      return self.brand

class Seller(models.Model):
   seller = models.CharField(max_length=100,unique=True)
   about_us = models.TextField(null=True,blank=True)
   join_date = models.DateTimeField(auto_now_add=datetime.now())
   def __str__(self):
      return self.seller

class AllFashion(models.Model):
   Products = models.OneToOneField('ecommapp.ProductInfo',on_delete=models.CASCADE,related_name='pros')
   Sellers = models.ManyToManyField('ecommapp.Seller_Product',related_name='selling_products')
   slug = models.SlugField(max_length=250,null=False, unique=True)
   gender = models.CharField(choices=GENDER_CHOICES, max_length=50)
   category = models.CharField(max_length=255)
   age = models.ManyToManyField(KidsAge,blank=True)
   card_image = models.ImageField(upload_to=user_directory_path) 
   title = models.CharField(max_length=100)   
   brand = models.ForeignKey(Brand,on_delete=models.CASCADE,null=True,related_name="all_brands")   
   def get_absolute_url(self):
        return reverse("product_info", kwargs={"slug": self.slug})
   def save(self, force_insert = False, force_update = True, using = False):
      if not self.slug:
            self.slug = slugify(self.title)
      return super().save()
   def __str__(self):
       return self.title

class ProductInfo(models.Model):
   Type = models.CharField(max_length=255,verbose_name='Type')
   Material = models.CharField(max_length=255,verbose_name='Material')
   Pattern = models.CharField(max_length=255,verbose_name='Pattern')
   Pocket = models.CharField(max_length=255,null=True,blank=True,verbose_name='Pocket')
   Sleeves = models.CharField(max_length=255,null=True,blank=True,verbose_name='Sleeves')
   Color = models.ManyToManyField(Color,verbose_name='Color')
   Neck = models.CharField(max_length=255,null=True,blank=True,verbose_name='Neck')
   Packet_Contains = models.CharField(max_length=100,null=True,verbose_name="Packet Contains")
   Occasion = models.CharField(max_length=255)
   Rise = models.CharField(choices=RISE_CHOICE,max_length=50,null=True,blank=True,verbose_name="Rise")
   Stretchable = models.BooleanField(null=True,blank=True,verbose_name="Stretchable")
   Care_instructions = models.CharField(max_length=200,null=True,blank=True,verbose_name="Care Instructions")
   Descriptions = models.TextField(null=True,verbose_name="Descriptions")
   Country = models.CharField(max_length=50,default="India")
   Manufacture = models.CharField(max_length=1000,null=True)
   def get_fields(self):
      val = []
      for f in self._meta.get_fields(): 
         if  getattr(self,f.name)!=None and f.name not in ('pros',
            'id','Type','Descriptions','Manufacture','Country'):
            val.append((f.verbose_name,(getattr(self, f.name))))
      return val 
      #getattr(self,f.name)!=None and f.name!='productdetail_ptr' and f.name!='Product' and f.name!='id' :

class Seller_Product(models.Model):
   seller = models.ForeignKey(Seller,on_delete=models.CASCADE) 
   size = models.ManyToManyField(Size,related_name='sizecharts')
   Return = models.IntegerField(default=7)
   specifications = models.ForeignKey(Size,on_delete=models.CASCADE,related_name='specifics',null=True)   
   dlvry_charges = models.CharField(max_length=100,default='FREE')
   upload_date = models.DateTimeField(auto_now_add=datetime.now())   
      
class EcomCart(models.Model):
   user = models.ForeignKey(User,on_delete=models.CASCADE)
   total_amnt = models.IntegerField(default=0)
   total_dscnt = models.IntegerField(default=0)
   total_qty = models.IntegerField(default=0)
   dlvry_chrg = models.CharField(max_length=30,default="FREE")
   date_created = models.DateTimeField(auto_now=True)

   def save(self, force_insert = True, force_update = False, using = False):
      if self.total_amnt >= 499 or self.dlvry_chrg == 0.0:
         self.dlvry_chrg = "FREE"
      return super().save()
   def __str__(self):
      return str(self.user)

class EcomCartItem(models.Model):
   cart = models.ForeignKey(EcomCart,on_delete=models.CASCADE,related_name="cart_ecom")
   cart_image=models.ImageField(null=True)
   title = models.CharField(max_length=60,null=True)
   quantity = models.IntegerField(default=1)
   size = models.ForeignKey(Size,on_delete=models.CASCADE,related_name='size_cart')
   brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
   seller = models.ForeignKey(Seller_Product,on_delete=models.CASCADE)
   delivery = models.CharField(max_length=30,default=0)
   total_price = models.IntegerField()
   total_mrp = models.IntegerField(default=0)
   carted_product = models.ForeignKey(AllFashion,on_delete=models.CASCADE,related_name='cartitems') 
   def save(self, force_insert = True, force_update = False, using = False):
      self.total_price = self.quantity * self.size.price
      self.total_mrp = self.quantity * self.size.mrp
      self.delivery = self.seller.dlvry_charges   
      return super().save()
   
class SaveForLater(models.Model):
   user = models.ForeignKey(User,on_delete=models.CASCADE)
   image=models.ImageField(null=True)
   title = models.CharField(max_length=60,null=True)
   size = models.ForeignKey(Size,on_delete=models.CASCADE)
   brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
   seller = models.ForeignKey(Seller_Product,on_delete=models.CASCADE)
   qty = models.IntegerField(default=1)
   all_pro = models.ForeignKey(AllFashion,on_delete=models.CASCADE)
 