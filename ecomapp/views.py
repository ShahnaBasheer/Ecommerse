from django.db.models import Count
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django import template
import json
from django.shortcuts import get_object_or_404
from . import models
from itertools import chain
from django.template.loader import render_to_string
from ecomapp.models import BoysCategory, BoysDetail,BoysFashion,GirlsCategory, GirlsDetail,GirlsFashion,MenCategory, MenDetail,MenFashion,WomenCategory,WomenDetail,WomenFashion,Size,KidsAge
# Create your views here.

def home(request):
    return render(request,'homepage.html')

def womentab(request):
    card_details = WomenFashion.objects.all()
    products = WomenCategory.objects.all()
    size = Size.objects.all()
    discounts = models.DISCOUNT_CHOICES
    #g_count = WomenFashion.objects.values('category__women').annotate(count = Count('id'))
    context = {
      'allproducts':{'category':products,'size':size,'discounts':discounts},
      'details':card_details,
    }
    return render(request,'women.html',context)
  
def mentab(request):
    card_details = MenFashion.objects.all()
    products = MenCategory.objects.all()
    size = Size.objects.all()
    discounts = models.DISCOUNT_CHOICES
    context = {
      'allproducts':{'category':products,'size':size,'discounts':discounts},
      'details':card_details,
    }
    return render(request,'men.html',context)

def filter_women(request):
    card_details = WomenFashion.objects.all()
    pro_list = request.GET.getlist('category[]')
    size_list = request.GET.getlist('size[]')
    discount_list = request.GET.getlist('discount[]')
    if len(pro_list) > 0:
      card_details = card_details.filter(category__women__in = pro_list).all().distinct()
    if len(size_list) > 0:
      card_details = card_details.filter(size__size__in = size_list).all().distinct()
    if len(discount_list) > 0:
      card_details = card_details.filter(discount__in = discount_list).all().distinct()
       #add __in columnname to filter list of values    
       #add getlist to take values as list      
    ajax = render_to_string('cards.html', {'details': card_details})
    return JsonResponse({'details': ajax})

def filter_men(request):
    card_details = MenFashion.objects.all()
    pro_list = request.GET.getlist('category[]')
    size_list = request.GET.getlist('size[]')
    discount_list = request.GET.getlist('discount[]')
    if len(pro_list) > 0:
      card_details = card_details.filter(category__men__in = pro_list).all().distinct() 
    if len(size_list) > 0:
      card_details = card_details.filter(size__size__in = size_list).all() .distinct()      
    if len(discount_list) > 0:
      card_details = card_details.filter(discount__in = discount_list).all().distinct()
    ajax = render_to_string('cards.html', {'details': card_details})
    return JsonResponse({'details': ajax})

def kidstab(request):
    kids_age = KidsAge.objects.all()  
    size = Size.objects.all()
    discounts = models.DISCOUNT_CHOICES
    products = GirlsCategory.objects.values('girls').union(BoysCategory.objects.values('boys'))
    card_details = list(chain(GirlsFashion.objects.all(),BoysFashion.objects.all()))
    context = {
      'allproducts':{'category':products,'age':kids_age,'size':size,'discounts':discounts},
      'details':card_details,
    }
    return render(request,'kids.html',context)

def filter_kids(request):
    girls_filt = GirlsFashion.objects.all()
    boys_filt = BoysFashion.objects.all()
    card_details = girls_filt.union(boys_filt)
    pro_list = request.GET.getlist('category[]')
    age_list = request.GET.getlist('age[]')
    size_list = request.GET.getlist('size[]')
    discount_list = request.GET.getlist('discount[]')
    if len(pro_list) > 0:
       girls_filt = girls_filt.filter(category__girls__in = pro_list).all().distinct()
       boys_filt = boys_filt.filter(category__boys__in = pro_list).all().distinct()
       card_details = girls_filt.union(boys_filt)
    if len(age_list) > 0:
       girls_filt = girls_filt.filter(age__age__in = age_list).all().distinct()
       boys_filt = boys_filt.filter(age__age__in = age_list).all().distinct()
       card_details = girls_filt.union(boys_filt)
    if len(size_list) > 0:
       girls_filt = girls_filt.filter(size__size__in = size_list).all().distinct()
       boys_filt = boys_filt.filter(size__size__in = size_list).all().distinct()
       card_details = girls_filt.union(boys_filt)
    if len(discount_list) > 0:
       girls_filt = girls_filt.filter(discount__in = discount_list).all().distinct()
       boys_filt = boys_filt.filter(discount__in = discount_list).all().distinct()
       card_details = girls_filt.union(boys_filt)
    ajax = render_to_string('cards.html',{'details':card_details}) 
    return JsonResponse({'details':ajax})

def filter_girls(request):
    card_details = GirlsFashion.objects.all()
    products = GirlsCategory.objects.all()
    kids_age = KidsAge.objects.all()
    size = Size.objects.all()
    discounts = models.DISCOUNT_CHOICES
    pro_list = request.GET.getlist('category[]')
    age_list = request.GET.getlist('age[]')
    size_list = request.GET.getlist('size[]')
    discount_list =request.GET.getlist('discount[]')
    if len(pro_list) > 0:
       card_details = card_details.filter(category__girls__in = pro_list).all().distinct()
    if len(age_list) > 0:
       card_details = card_details.filter(age__age__in = age_list).all().distinct()
    if len(size_list) > 0:
       card_details = card_details.filter(size__size__in = size_list).all().distinct()
    if len(discount_list) > 0:
      card_details = card_details.filter(discount__in = discount_list).all().distinct()
    ajax = render_to_string('cards.html',{'details':card_details})
    category = render_to_string('kidscategory.html',{'allproducts':{'category':products}})
    ages = render_to_string('kidsage.html',{'allproducts':{'age':kids_age}})
    sizes = render_to_string('kidsize.html',{'allproducts':{'size':size}})
    offers = render_to_string('kidsdiscount.html',{'allproducts':{'discounts':discounts}})
    return JsonResponse({'details':ajax,'allcategory':category,'allages':ages,'allsizes':sizes,'alloffers':offers})

def filter_boys(request):
    card_details = BoysFashion.objects.all()
    products = BoysCategory.objects.all()
    kids_age = KidsAge.objects.all()
    size = Size.objects.all()
    discounts = models.DISCOUNT_CHOICES
    pro_list = request.GET.getlist('category[]')
    age_list = request.GET.getlist('age[]')
    size_list = request.GET.getlist('size[]')
    discount_list = request.GET.getlist('discount[]')
    if len(pro_list) > 0:
       card_details = card_details.filter(category__boys__in = pro_list).all().distinct()
    if len(age_list) > 0:
       card_details = card_details.filter(age__age__in = age_list).all().distinct()
    if len(size_list) > 0:
       card_details = card_details.filter(size__size__in = size_list).all().distinct()
    if len(discount_list) > 0:
      card_details = card_details.filter(discount__in = discount_list).all().distinct()
    ajax = render_to_string('cards.html',{'details':card_details})
    category = render_to_string('kidscategory.html',{'allproducts':{'category':products}})
    ages = render_to_string('kidsage.html',{'allproducts':{'age':kids_age}})
    sizes = render_to_string('kidsize.html',{'allproducts':{'size':size}})
    offers = render_to_string('kidsdiscount.html',{'allproducts':{'discounts':discounts}})
    return JsonResponse({'details':ajax,'allcategory':category,'allages':ages,'allsizes':sizes,'alloffers':offers})

def product_info(request,product_id):
    products = ""
    infotag = request.GET['info']
    if infotag == 'women':
      products = WomenFashion.objects.get(pk = product_id)
      product_details = get_object_or_404(WomenDetail, Product__id= product_id)         
    if infotag =='men':
      products = MenFashion.objects.get(pk = product_id)
      product_details = get_object_or_404(MenDetail, Product__id= product_id)
    if infotag == 'girls':
      products = GirlsFashion.objects.get(pk = product_id)
      product_details = get_object_or_404(GirlsDetail, Product__id= product_id)
    if infotag == 'boys':
      products = BoysFashion.objects.get(pk = product_id)
      product_details = get_object_or_404(BoysDetail, Product__id= product_id)
    context = {
      'details':products,
      'productdetails':product_details,
    }  
    return render(request,'product-info.html',context)

def cart(request):
    return render(request,'cart.html')
#When querying a ForeignKey field, you 'normally' pass an instance of the model
#like this for example,
# x = MenCategory.objects.get(men=proname) 
#card_details = MenFashion.objects.filter(category= x).all
#You can however, use __ (double underscore) to 'hop' across and query a specific field.
#card_details = WomenFashion.objects.filter(category__men = proname).all