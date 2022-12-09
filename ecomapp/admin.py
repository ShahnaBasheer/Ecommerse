
from django.contrib import admin
from . models import AllFashion,Brand, Category,Color, EcomCart, EcomCartItem, Pattern,KidsAge,Material,Neck,Occasion,Pocket, ProductInfo,SaveForLater, Seller,Size,Sleeve
# Register your models here.


admin.site.register(Category)
admin.site.register(Material)
admin.site.register(Pattern)
admin.site.register(Sleeve)
admin.site.register(Color)
admin.site.register(Neck)
admin.site.register(Pocket)
admin.site.register(Occasion)
admin.site.register(KidsAge)



class AllFashionAdmin(admin.ModelAdmin):
  list_display = ('id','gender','category','brand','title','price','mrp','discount',
                 'card_image','dlvry_charges','upload_date')
  list_editable = ('gender','brand','category','title','price','mrp','discount',
                 'card_image','dlvry_charges')
  prepopulated_fields = {"slug": ("title",)}
admin.site.register(AllFashion,AllFashionAdmin)


class ProductInfoAdmin(admin.ModelAdmin):
  list_display = ('id','Product','Type','Material','Pattern','Sleeves','Pocket','Neck',
                  'Rise','Occasion','Packet_Contains','Stretchable','Manufacture','Country','Return')
  list_editable = ('Product','Material','Type','Pattern','Sleeves','Pocket','Neck',
                  'Rise','Occasion','Packet_Contains','Stretchable','Manufacture','Country','Return')
admin.site.register(ProductInfo,ProductInfoAdmin)

class SizeAdmin(admin.ModelAdmin):
  list_display = ('id','size')
admin.site.register(Size,SizeAdmin)

class BrandAdmin(admin.ModelAdmin):
  list_display = ('id','brand','about')
admin.site.register(Brand,BrandAdmin)

class EcomCartAdmin(admin.ModelAdmin):
  list_display = ('id','user','total_amnt','total_dscnt','total_qty','dlvry_chrg','date_created')
admin.site.register(EcomCart,EcomCartAdmin)

class ECartItemAdmin(admin.ModelAdmin):
  list_display = ('id','brand','cart_image','title','size','quantity','total_price','total_mrp','delivery','seller')
admin.site.register(EcomCartItem,ECartItemAdmin)

class SellerAdmin(admin.ModelAdmin):
  list_display = ('id','seller','about_us','join_date')
admin.site.register(Seller,SellerAdmin)

class SaveForLaterAdmin(admin.ModelAdmin):
  list_display = ('id','brand','image','title','size','price','mrp','qty','seller')
admin.site.register(SaveForLater,SaveForLaterAdmin)