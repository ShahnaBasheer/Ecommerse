from django.db import models
from django.contrib.auth.models import User
import math
from django.utils.text import slugify
from django.urls import reverse
# Create your models here.

class Category(models.Model):
   category = models.CharField(max_length=50,unique=True)
   def __str__(self):
      return self.category

class KidsAge(models.Model):
   age = models.CharField(max_length=50,unique=True)
   def __str__(self):
      return self.age

class Size(models.Model):
   size = models.CharField(max_length=50,unique=True)   
   def __str__(self):
      return self.size

DISCOUNT_CHOICES = [
   ("10", "10% And Above"),
   ("20", "20% And Above"),
   ("30", "30% And Above"),
   ("40", "40% And Above"),
   ("50", "50% And Above"),
   ("60", "60% And Above"),
   ("70", "70% And Above"),
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

class Material(models.Model):
   material = models.CharField(max_length=255,unique=True)
   def __str__(self):
      return self.material

class Pattern(models.Model):
   pattern = models.CharField(max_length=255,unique=True)
   def __str__(self):
      return self.pattern

class Pocket(models.Model):
   pocket = models.CharField(max_length=255,unique=True)
   def __str__(self):
      return self.pocket

class Sleeve(models.Model):
   sleeves = models.CharField(max_length=255,unique=True)
   def __str__(self):
      return self.sleeves

class Color(models.Model):
   color = models.CharField(max_length=255,unique=True)
   def __str__(self):
      return self.color

class Neck(models.Model):
   neck = models.CharField(max_length=255,unique=True)
   def __str__(self):
      return self.neck

class Occasion(models.Model):
   occasion = models.CharField(max_length=255,unique=True)
   def __str__(self):
      return self.occasion

class Brand(models.Model):
   brand = models.CharField(max_length=255,unique=True)
   about = models.TextField(null=True,blank=True)
   def __str__(self):
      return self.brand

class Seller(models.Model):
   seller = models.CharField(max_length=100,unique=True)
   about_us = models.TextField(null=True,blank=True)
   join_date = models.DateTimeField(auto_now=True)
   def __str__(self):
      return self.seller

GENDER_CHOICES = [
   ("girls","girls"),
   ("boys","boys"),
   ("women","women"),
   ("men","men"),
]

class AllFashion(models.Model):
   slug = models.SlugField(max_length=250,null=False, unique=True)
   gender = models.CharField(choices=GENDER_CHOICES, max_length=50)
   category = models.ForeignKey(Category, on_delete=models.CASCADE)
   age = models.ManyToManyField(KidsAge,blank=True)
   card_image = models.ImageField(upload_to=user_directory_path) 
   title = models.CharField(max_length=60,unique=True)
   price = models.IntegerField()
   mrp = models.IntegerField(default=0)
   dlvry_charges = models.CharField(max_length=100,default='FREE')
   upload_date = models.DateTimeField(auto_now=True)
   size = models.ManyToManyField(Size,blank=True)
   discount = models.CharField(max_length=100,null=True,blank=True)
   brand = models.ForeignKey(Brand,on_delete=models.CASCADE,null=True,related_name="all_brands")
   
   def get_absolute_url(self):
        return reverse("product_info", kwargs={"slug": self.slug})

   def save(self, force_insert = False, force_update = True, using = False):
      if not self.slug:
            self.slug = slugify(self.title)
      self.discount = math.floor((self.mrp - self.price)/self.mrp * 100) 
      return super().save()

   def __str__(self):
       return self.title


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
   cart = models.ForeignKey(EcomCart,on_delete=models.CASCADE)
   cart_image=models.ImageField(null=True)
   title = models.CharField(max_length=60,null=True)
   quantity = models.IntegerField(default=1)
   size = models.ForeignKey(Size,on_delete=models.CASCADE,null=True,blank=True)
   brand = models.ForeignKey(Brand,on_delete=models.CASCADE,null=True)
   seller = models.ForeignKey(Seller,on_delete=models.CASCADE,null=True)
   delivery = models.CharField(max_length=30,default=0)
   total_price = models.IntegerField()
   total_mrp = models.IntegerField(default=0)
   products = models.ForeignKey(AllFashion,on_delete=models.CASCADE,related_name='cartitems')

   def save(self, force_insert = True, force_update = False, using = False):
      self.total_price = self.quantity * self.products.price
      self.total_mrp = self.quantity * self.products.mrp
      self.delivery = self.products.dlvry_charges
      return super().save()

RISE_CHOICE= [
      ('Mid Waist','Mid Waist'),
      ('Low Waist','Low Waist'),
      ('High Waist','High Waist'),
]

class ProductInfo(models.Model):
   Product = models.OneToOneField(AllFashion,on_delete=models.CASCADE,related_name='pros')
   Type = models.ForeignKey(Category,max_length=50,on_delete=models.CASCADE)
   Material = models.ForeignKey(Material,max_length=50,null=True,on_delete=models.CASCADE,verbose_name="Material")
   Pattern = models.ForeignKey(Pattern,max_length=50,null=True,on_delete=models.CASCADE,verbose_name="Pattern")
   Pocket = models.ForeignKey(Pocket,max_length=50,null=True,blank=True,on_delete=models.CASCADE,verbose_name="Pocket")
   Sleeves = models.ForeignKey(Sleeve,max_length=50,null=True,blank=True,on_delete=models.CASCADE,verbose_name="sleeves")
   Color = models.ManyToManyField(Color,verbose_name="Color")
   Neck = models.ForeignKey(Neck,max_length=50,null=True,blank=True,on_delete=models.CASCADE,verbose_name="Neck")
   Packet_Contains = models.CharField(max_length=100,null=True,verbose_name="Packet Contains")
   Occasion = models.ForeignKey(Occasion,max_length=50,null=True,on_delete=models.CASCADE,verbose_name="Occasion")
   Rise = models.CharField(choices=RISE_CHOICE,max_length=50,null=True,blank=True,verbose_name="Rise")
   Stretchable = models.BooleanField(null=True,blank=True,verbose_name="Stretchable")
   Care_instructions = models.CharField(max_length=200,null=True,blank=True,verbose_name="Care Instructions")
   Descriptions = models.TextField(null=True,verbose_name="Descriptions")
   Sellers = models.ManyToManyField(Seller)
   Country = models.CharField(max_length=50,default="India")
   Manufacture = models.CharField(max_length=1000,null=True)
   Return = models.IntegerField(default=7)
   def get_fields(self):
      val = []
      for f in self._meta.get_fields(): 
         if  getattr(self,f.name)!=None and f.name not in ('Product',
            'id','Type','Descriptions','Sellers','Manufacture','Country','Return'):
            val.append((f.verbose_name,(getattr(self, f.name))))
      return val 
      #getattr(self,f.name)!=None and f.name!='productdetail_ptr' and f.name!='Product' and f.name!='id' :


class SaveForLater(models.Model):
  
   user = models.ForeignKey(User,on_delete=models.CASCADE)
   image=models.ImageField(null=True)
   title = models.CharField(max_length=60,null=True)
   size = models.ForeignKey(Size,on_delete=models.CASCADE,null=True,blank=True)
   brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
   seller = models.ForeignKey(Seller,on_delete=models.CASCADE)
   qty = models.IntegerField(default=1)
   price = models.IntegerField()
   mrp = models.IntegerField(default=0)
   all_pro = models.ForeignKey(AllFashion,on_delete=models.CASCADE)
 