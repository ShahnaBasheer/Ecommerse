
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . models import AllFashion,Brand,Color,CustomUser, EcomCart, EcomCartItem, KidsAge,ProductInfo, SaveForLater,Seller, Seller_Product,Size
# Register your models here.

class CustomUserAdmin(UserAdmin):
  list_display = (
        'username', 'email', 'first_name', 'last_name', 'gender',
        'phone_no', 'dob',
        )
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(KidsAge)
admin.site.register(Color)
  
class AllFashionAdmin(admin.ModelAdmin):
  list_display = ('id','Products','gender','age','category','brand','title','sellers','card_image')
  list_editable = ('gender','age','category','brand','title','card_image')
  prepopulated_fields = {"slug": ("title",)}

  def sellers(self, obj):
        return ",".join([str(a.seller) for a in obj.Sellers.all()])
  def age(self, obj):
        return ",".join([str(a) for a in obj.age.all()])  

admin.site.register(AllFashion,AllFashionAdmin)


class ProductInfoAdmin(admin.ModelAdmin):
  list_display = ('id','Material','Pattern','Sleeves','Pocket','Neck','colors',
                  'Rise','Occasion','Packet_Contains','Stretchable','Manufacture','Country')
  list_editable = ('Material','Pattern','Sleeves','Pocket','Neck',
                  'Rise','Occasion','Packet_Contains','Stretchable','Manufacture','Country')
  def colors(self, obj):
        return ",".join([str(a) for a in obj.Color.all()])  

admin.site.register(ProductInfo,ProductInfoAdmin)

class SizeAdmin(admin.ModelAdmin):
  list_display = ('id','sizes','price','mrp','discount','discnt_cat','stock')
admin.site.register(Size,SizeAdmin)

class BrandAdmin(admin.ModelAdmin):
  list_display = ('id','brand','about')
admin.site.register(Brand,BrandAdmin)

class EcomCartAdmin(admin.ModelAdmin):
  list_display = ('id','user','total_amnt','total_dscnt','total_qty','dlvry_chrg','date_created')
admin.site.register(EcomCart,EcomCartAdmin)

class ECartItemAdmin(admin.ModelAdmin):
  list_display = ('id','cart','brand','cart_image','title','size','quantity','total_price','total_mrp','delivery','seller')
admin.site.register(EcomCartItem,ECartItemAdmin)

class SellerAdmin(admin.ModelAdmin):
  list_display = ('id','seller','about_us','join_date')
admin.site.register(Seller,SellerAdmin)

class Seller_ProductAdmin(admin.ModelAdmin):  
  list_display = ('id','seller','Return','sizes','specifications','dlvry_charges','upload_date')
  def sizes(self, obj):
        return ",".join([str(a) for a in obj.size.all()]) 
admin.site.register(Seller_Product,Seller_ProductAdmin)

class SaveForLaterAdmin(admin.ModelAdmin):
  list_display = ('id','brand','image','title','size','qty','seller')
admin.site.register(SaveForLater,SaveForLaterAdmin)