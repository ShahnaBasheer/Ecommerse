
from django.contrib import admin
from . models import BoysDetail,Color,GirlsDetail,MenDetail,Pattern,KidsAge,Material,Neck,Occasion,Pocket,Size,Sleeve,WomenCategory,MenCategory,GirlsCategory,BoysCategory,WomenFashion,MenFashion,GirlsFashion,BoysFashion,WomenDetail
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

class WomenAdmin(admin.ModelAdmin):
  list_display = ('id','category','seller','description','price','card_image',
                 'discount','upload_date')
admin.site.register(WomenFashion,WomenAdmin)

class MenAdmin(admin.ModelAdmin):
  list_display = ('id','category','seller','description','price','card_image',
                 'discount','upload_date')
admin.site.register(MenFashion,MenAdmin)

class GirlsAdmin(admin.ModelAdmin):
  list_display = ('id','category','seller','description','price','card_image',
                  'discount','upload_date')
admin.site.register(GirlsFashion,GirlsAdmin)

class BoysAdmin(admin.ModelAdmin):
  list_display = ('id','category','seller','description','price','card_image',
                  'discount','upload_date')
admin.site.register(BoysFashion,BoysAdmin)


class WomenDetailAdmin(admin.ModelAdmin):
  list_display = ('id','Product','Type','Material','Pattern','Sleeves','Pocket','Neck',
                  'Rise','Occasion','Packet_Contains','Stretchable')
admin.site.register(WomenDetail,WomenDetailAdmin)

class MenProductAdmin(admin.ModelAdmin):
  list_display = ('id','Product','Type','Material','Pattern','Sleeves','Pocket','Neck',
                  'Rise','Occasion','Packet_Contains','Stretchable')
admin.site.register(MenDetail,MenProductAdmin)

class GirlsDetailAdmin(admin.ModelAdmin):
  list_display = ('id','Product','Type','Material','Pattern','Sleeves','Pocket','Neck',
                  'Rise','Occasion','Packet_Contains','Stretchable')
admin.site.register(GirlsDetail,GirlsDetailAdmin)

class BoysDetailAdmin(admin.ModelAdmin):
  list_display = ('id','Product','Type','Material','Pattern','Sleeves','Pocket','Neck',
                  'Rise','Occasion','Packet_Contains','Stretchable')                  
admin.site.register(BoysDetail,BoysDetailAdmin)
