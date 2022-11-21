from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import math
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

# Create your models here.

class WomenCategory(models.Model):
   women = models.CharField(max_length=50,unique=True)
   def __str__(self):
      return self.women

class MenCategory(models.Model):
   men = models.CharField(max_length=50,unique=True)
   def __str__(self):
      return self.men

class GirlsCategory(models.Model):
   girls = models.CharField(max_length=50,unique=True)
   def __str__(self):
      return self.girls

class BoysCategory(models.Model):
   boys = models.CharField(max_length=50,unique=True) 
   def __str__(self):
      return self.boys

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
    if isinstance(instance,WomenFashion):
      x = "women"
    elif isinstance(instance,MenFashion):
      x = "men"
    elif isinstance(instance,GirlsFashion):
      x = "girls"
    elif isinstance(instance,BoysFashion):
      x = "boys"
    else:
      pass
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


#The base class for all 4 databases
class Cart(models.Model):
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

class CartItem(models.Model):
   cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
   cart_image=models.ImageField(null=True)
   title = models.CharField(max_length=60,null=True)
   content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
   quantity = models.IntegerField(default=1)
   size = models.ForeignKey(Size,on_delete=models.CASCADE,null=True)
   brand = models.ForeignKey(Brand,on_delete=models.CASCADE,null=True)
   seller = models.ForeignKey(Seller,on_delete=models.CASCADE,null=True)
   delivery = models.CharField(max_length=30,default=0)
   total_price = models.IntegerField()
   total_mrp = models.IntegerField(default=0)
   object_id = models.PositiveIntegerField()
   content_object = GenericForeignKey('content_type', 'object_id')
   
   def save(self, force_insert = True, force_update = False, using = False):
      self.total_price = self.quantity * self.content_object.price
      self.total_mrp = self.quantity * self.content_object.mrp
      self.delivery = self.content_object.dlvry_charges
      return super().save()
        
class iambase(models.Model):
   card_image = models.ImageField(upload_to=user_directory_path) 
   brand = models.ForeignKey(Brand,on_delete=models.CASCADE,null=True)
   title = models.CharField(max_length=60)
   price = models.IntegerField()
   mrp = models.IntegerField(default=0)
   dlvry_charges = models.CharField(max_length=100,default='FREE')
   upload_date = models.DateTimeField(auto_now=True)
   size = models.ManyToManyField(Size)
   discount = models.CharField(max_length=100,null=True,blank=True)
   cartitems = GenericRelation(CartItem,related_query_name='cartitems') 

   def save(self, force_insert = False, force_update = True, using = False):
      self.discount = math.floor((self.mrp - self.price)/self.mrp * 100)
      return super().save()
      
   class Meta:
     abstract = True

class WomenFashion(iambase):
    category = models.ForeignKey(WomenCategory, on_delete=models.CASCADE)   
    gender = "women"
    def __str__(self):
       return self.title

class MenFashion(iambase):
    category = models.ForeignKey(MenCategory, on_delete=models.CASCADE)
    gender = "men"
    def __str__(self):
       return self.title

class GirlsFashion(iambase):
    category = models.ForeignKey(GirlsCategory, on_delete=models.CASCADE)
    age = models.ManyToManyField(KidsAge)
    gender = "girls"
    def __str__(self):
       return self.title

class BoysFashion(iambase):
    category = models.ForeignKey(BoysCategory, on_delete=models.CASCADE)
    age = models.ManyToManyField(KidsAge)
    gender = "boys"
    def __str__(self):
       return self.title

RISE_CHOICE= [
      ('Mid Rise','Mid Rise'),
      ('Low Rise','Low Rise'),
      ('High Rise','High Rise'),
]

class ProductDetail(models.Model):
   Material = models.ForeignKey(Material,max_length=50,null=True,on_delete=models.CASCADE,verbose_name="Material")
   Pattern = models.ForeignKey(Pattern,max_length=50,null=True,on_delete=models.CASCADE,verbose_name="Pattern")
   Pocket = models.ForeignKey(Pocket,max_length=50,null=True,on_delete=models.CASCADE,blank=True,verbose_name="Pocket")
   Sleeves = models.ForeignKey(Sleeve,max_length=50,null=True,on_delete=models.CASCADE,blank=True,verbose_name="Sleeves")
   Color = models.ManyToManyField(Color,verbose_name="Color")
   Neck = models.ForeignKey(Neck,max_length=50,null=True,on_delete=models.CASCADE,blank=True,verbose_name="Neck")
   Packet_Contains = models.CharField(max_length=100,null=True,blank=True,verbose_name="Packet Contains")
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
         if  getattr(self,f.name)!=None and f.name not in ('productdetail_ptr','Product',
            'id','Type','Descriptions','Sellers','Manufacture','Country','Return'):
            val.append((f.verbose_name,(getattr(self, f.name))))
      return val 
      #getattr(self,f.name)!=None and f.name!='productdetail_ptr' and f.name!='Product' and f.name!='id' :

class WomenDetail(ProductDetail):
   Product = models.OneToOneField(WomenFashion,on_delete=models.CASCADE)
   Type = models.ForeignKey(WomenCategory,max_length=50,on_delete=models.CASCADE)
   

class MenDetail(ProductDetail):
   Product = models.OneToOneField(MenFashion,on_delete=models.CASCADE)
   Type = models.ForeignKey(MenCategory,max_length=50,on_delete=models.CASCADE)

class GirlsDetail(ProductDetail):
   Product = models.OneToOneField(GirlsFashion,on_delete=models.CASCADE)
   Type = models.ForeignKey(GirlsCategory,max_length=50,on_delete=models.CASCADE)

class BoysDetail(ProductDetail):
   Product = models.OneToOneField(BoysFashion,on_delete=models.CASCADE)
   Type = models.ForeignKey(BoysCategory,max_length=50,on_delete=models.CASCADE)


 