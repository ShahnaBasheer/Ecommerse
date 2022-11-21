
from django.contrib import admin
from . models import BoysDetail, Brand, Cart, CartItem, Color,GirlsDetail,MenDetail,Pattern,KidsAge,Material,Neck,Occasion,Pocket, Seller,Size,Sleeve,WomenCategory,MenCategory,GirlsCategory,BoysCategory,WomenFashion,MenFashion,GirlsFashion,BoysFashion,WomenDetail
# Register your models here.

admin.site.register(BoysCategory)
admin.site.register(GirlsCategory)
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
admin.site.register(Size)

class BrandAdmin(admin.ModelAdmin):
  list_display = ('id','brand','about')
admin.site.register(Brand,BrandAdmin)

class WomenAdmin(admin.ModelAdmin):
  list_display = ('id','category','brand','title','price','mrp','discount',
                 'card_image','dlvry_charges','upload_date')
  list_editable = ('category','brand','title','price','mrp','discount',
                 'card_image','dlvry_charges')
admin.site.register(WomenFashion,WomenAdmin)

class MenAdmin(admin.ModelAdmin):
  list_display = ('id','category','brand','title','price','mrp','discount',
                 'card_image','dlvry_charges','upload_date')
  list_editable = ('category','brand','title','price','mrp','discount',
                 'card_image','dlvry_charges')
admin.site.register(MenFashion,MenAdmin)

class GirlsAdmin(admin.ModelAdmin):
  list_display = ('id','category','brand','title','price','mrp','discount',
                 'card_image','dlvry_charges','upload_date')
admin.site.register(GirlsFashion,GirlsAdmin)

class BoysAdmin(admin.ModelAdmin):
  list_display = ('id','category','brand','title','price','mrp','discount',
                 'card_image','dlvry_charges','upload_date')
admin.site.register(BoysFashion,BoysAdmin)
  

class WomenDetailAdmin(admin.ModelAdmin):
  list_display = ('id','Product','Type','Material','Pattern','Sleeves','Pocket','Neck',
                  'Rise','Occasion','Packet_Contains','Stretchable','Manufacture','Country','Return')
  list_editable = ('Type','Material','Pattern','Sleeves','Pocket','Neck',
                  'Rise','Occasion','Packet_Contains','Stretchable','Manufacture','Country','Return')
admin.site.register(WomenDetail,WomenDetailAdmin)

class MenDetailAdmin(admin.ModelAdmin):
  list_display = ('id','Product','Type','Material','Pattern','Sleeves','Pocket','Neck',
                 'Rise','Occasion','Packet_Contains','Stretchable','Manufacture','Country','Return')
admin.site.register(MenDetail,MenDetailAdmin)

class GirlsDetailAdmin(admin.ModelAdmin):
  list_display = ('id','Product','Type','Material','Pattern','Sleeves','Pocket','Neck','Rise',
                  'Occasion','Packet_Contains','Stretchable','Manufacture','Country','Return')
admin.site.register(GirlsDetail,GirlsDetailAdmin)

class BoysDetailAdmin(admin.ModelAdmin):
  list_display = ('id','Product','Type','Material','Pattern','Sleeves','Pocket','Neck',
                  'Rise','Occasion','Packet_Contains','Stretchable','Manufacture','Country','Return')
  list_editable = ('Type','Material','Pattern','Sleeves','Pocket','Neck',
                  'Rise','Occasion','Packet_Contains','Stretchable','Manufacture','Country','Return')                                    
admin.site.register(BoysDetail,BoysDetailAdmin)

class CartAdmin(admin.ModelAdmin):
  list_display = ('id','user','total_amnt','total_dscnt','total_qty','dlvry_chrg','date_created')
admin.site.register(Cart,CartAdmin)

class CartItemAdmin(admin.ModelAdmin):
  list_display = ('id','cart','brand','cart_image','title','size','quantity','total_price','total_mrp','delivery','seller')
admin.site.register(CartItem,CartItemAdmin)

class SellerAdmin(admin.ModelAdmin):
  list_display = ('id','seller','about_us','join_date')
admin.site.register(Seller,SellerAdmin)
