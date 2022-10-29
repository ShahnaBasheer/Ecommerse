from django.db import models
from django.contrib.auth.models import User
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
   ("10%", "10% And Above"),
   ("20%", "20% And Above"),
   ("30%", "30% And Above"),
   ("40%", "40% And Above"),
   ("50%", "50% And Above"),
   ("60%", "60% And Above"),
   ("70%", "70% And Above"),
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

#The base class for all 4 databases

class iambase(models.Model):
   seller = models.CharField(max_length=50)
   description = models.CharField(max_length=60)
   price = models.IntegerField()
   card_image = models.ImageField(upload_to=user_directory_path) 
   upload_date = models.DateTimeField(auto_now=True)
   size = models.ManyToManyField(Size)
   discount = models.CharField(choices=DISCOUNT_CHOICES,max_length=100,null=True,blank=True)
 
   class Meta:
     abstract = True

class WomenFashion(iambase):
    category = models.ForeignKey(WomenCategory, on_delete=models.CASCADE)
    gender = "women"
    def __str__(self):
       return "object"+" "+str(self.id)

class MenFashion(iambase):
    category = models.ForeignKey(MenCategory, on_delete=models.CASCADE)
    gender = "men"
    def __str__(self):
       return "object"+" "+str(self.id)

class GirlsFashion(iambase):
    category = models.ForeignKey(GirlsCategory, on_delete=models.CASCADE)
    age = models.ManyToManyField(KidsAge)
    gender = "girls"
    def __str__(self):
       return "object"+" "+str(self.id)

class BoysFashion(iambase):
    category = models.ForeignKey(BoysCategory, on_delete=models.CASCADE)
    age = models.ManyToManyField(KidsAge)
    gender = "boys"
    def __str__(self):
       "object"+" "+str(self.id)

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
   def get_fields(self):
      val = []
      for f in self._meta.get_fields(): 
         if  getattr(self,f.name)!=None and f.name not in ('productdetail_ptr','Product','id','Color','Type','Descriptions'):
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


