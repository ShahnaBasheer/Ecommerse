
from django.contrib import admin
from . models import Brand, Cart, CartItem, Color,KidsCategory, KidsDetail, KidsFashion,MenDetail,Pattern,KidsAge,Material,Neck,Occasion,Pocket, SaveItForLater, Seller,Size,Sleeve,WomenCategory,MenCategory,WomenFashion,MenFashion,WomenDetail
# Register your models here.

admin.site.register(KidsCategory)
admin.site.register(WomenCategory)
admin.site.register(MenCategory)
admin.site.register(Material)
admin.site.register(Pattern)
admin.site.register(Sleeve)
admin.site.register(Color)
admin.site.register(Neck)
admin.site.register(Pocket)
admin.site.register(Occasion)
admin.site.register(KidsAge)

class SizeAdmin(admin.ModelAdmin):
  list_display = ('id','size')
admin.site.register(Size,SizeAdmin)

class BrandAdmin(admin.ModelAdmin):
  list_display = ('id','brand','about')
admin.site.register(Brand,BrandAdmin)

class WomenAdmin(admin.ModelAdmin):
  list_display = ('id','category','brand','title','price','mrp','discount',
                 'card_image','dlvry_charges','upload_date')
admin.site.register(WomenFashion,WomenAdmin)

class MenAdmin(admin.ModelAdmin):
  list_display = ('id','category','brand','title','price','mrp','discount',
                 'card_image','dlvry_charges','upload_date')
admin.site.register(MenFashion,MenAdmin)

class KidsAdmin(admin.ModelAdmin):
  list_display = ('id','gender','category','brand','title','price','mrp','discount',
                 'card_image','dlvry_charges','upload_date')
  list_editable = ('gender','category','brand','title','price','mrp','discount',
                 'card_image','dlvry_charges')
admin.site.register(KidsFashion,KidsAdmin)

class WomenDetailAdmin(admin.ModelAdmin):
  list_display = ('id','Product','Type','Material','Pattern','Sleeves','Pocket','Neck',
                  'Rise','Occasion','Packet_Contains','Stretchable','Manufacture','Country','Return')
admin.site.register(WomenDetail,WomenDetailAdmin)

class MenDetailAdmin(admin.ModelAdmin):
  list_display = ('id','Product','Type','Material','Pattern','Sleeves','Pocket','Neck',
                 'Rise','Occasion','Packet_Contains','Stretchable','Manufacture','Country','Return')
admin.site.register(MenDetail,MenDetailAdmin)

class KidsDetailAdmin(admin.ModelAdmin):
  list_display = ('id','Product','Type','Material','Pattern','Sleeves','Pocket','Neck',
                  'Rise','Occasion','Packet_Contains','Stretchable','Manufacture','Country','Return')
admin.site.register(KidsDetail,KidsDetailAdmin)

class CartAdmin(admin.ModelAdmin):
  list_display = ('id','user','total_amnt','total_dscnt','total_qty','dlvry_chrg','date_created')
admin.site.register(Cart,CartAdmin)

class CartItemAdmin(admin.ModelAdmin):
  list_display = ('id','cart','brand','cart_image','title','size','quantity','total_price','total_mrp','delivery','seller')
admin.site.register(CartItem,CartItemAdmin)

class SellerAdmin(admin.ModelAdmin):
  list_display = ('id','seller','about_us','join_date')
admin.site.register(Seller,SellerAdmin)

class SaveItForLaterAdmin(admin.ModelAdmin):
  list_display = ('id','user','brand','image','title','size','price','mrp','qty','seller')
admin.site.register(SaveItForLater,SaveItForLaterAdmin)