from django.contrib import admin
from . models import WomenCategory,MenCategory,GirlsCategory,BoysCategory,WomenFashion,MenFashion,GirlsFashion,BoysFashion,KidsAge,Size

# Register your models here.
class WomenCategoryAdmin(admin.ModelAdmin):
  list_display = ('id','women')
admin.site.register(WomenCategory,WomenCategoryAdmin)

class MenCategoryAdmin(admin.ModelAdmin):
  list_display = ('id','men')
admin.site.register(MenCategory,MenCategoryAdmin)

class GirlsCategoryAdmin(admin.ModelAdmin):
  list_display = ('id','kids')
admin.site.register(GirlsCategory,GirlsCategoryAdmin)

class BoysCategoryAdmin(admin.ModelAdmin):
  list_display = ('id','kids')
admin.site.register(BoysCategory,BoysCategoryAdmin)

class WomenAdmin(admin.ModelAdmin):
  list_display = ('id','category','seller','description','price','card_image','upload_date')
admin.site.register(WomenFashion,WomenAdmin)

class MenAdmin(admin.ModelAdmin):
  list_display = ('id','category','seller','description','price','card_image','upload_date')
admin.site.register(MenFashion,MenAdmin)

class GirlsAdmin(admin.ModelAdmin):
  list_display = ('id','category','seller','description','price','card_image','upload_date')
admin.site.register(GirlsFashion,GirlsAdmin)

class BoysAdmin(admin.ModelAdmin):
  list_display = ('id','category','seller','description','price','card_image','upload_date')
admin.site.register(BoysFashion,BoysAdmin)

class KidsAgeAmin(admin.ModelAdmin):
  list_display = ('id','age')
admin.site.register(KidsAge,KidsAgeAmin)

class SizeAdmin(admin.ModelAdmin):
  list_display = ('id','size')
admin.site.register(Size,SizeAdmin)