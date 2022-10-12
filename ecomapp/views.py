from django.shortcuts import render,redirect
from django.http import JsonResponse
import json
from django.template.loader import render_to_string
from ecomapp.models import BoysCategory, BoysFashion, GirlsCategory, GirlsFashion, MenCategory, MenFashion, WomenCategory, WomenFashion
# Create your views here.

def home(request):
    return render(request,'homepage.html')

def womentab(request):
    card_details = WomenFashion.objects.all()
    products = WomenCategory.objects.all()
    context = {
      'allproducts':products,
      'details':card_details,  
      }
    return render(request,'women.html',context)
  
def mentab(request):
    card_details = MenFashion.objects.all()
    products = MenCategory.objects.all()
    context = {
      'allproducts':products,
      'details':card_details,
    }
    return render(request,'men.html',context)

def kidstab(request):
    girls_details = GirlsFashion.objects.all()
    boys_details = BoysFashion.objects.all()
    gproducts = GirlsCategory.objects.all()
    bproducts = BoysCategory.objects.all()
    context = {
      'girls_products':gproducts,
      'boys_products':bproducts,
      'girls_details':girls_details,
      'boys_details':boys_details,
      
    }
    return render(request,'kids.html')

def filter_women(request):
    card_details = WomenFashion.objects.all()
    pro_list = request.GET.getlist('category[]')
    if len(pro_list) > 0:
      card_details = WomenFashion.objects.filter(category__women__in = pro_list).all() 
       #add __in columnname to filter list of values    
       #add getlist to take values as list      
    ajax = render_to_string('cards.html', {'details': card_details})
    return JsonResponse({'details': ajax})

def filter_men(request):
    card_details = MenFashion.objects.all()
    pro_list = request.GET.getlist('category[]')
    if len(pro_list) > 0:
      card_details = MenFashion.objects.filter(category__men__in = pro_list).all()       
    ajax = render_to_string('cards.html', {'details': card_details})
    return JsonResponse({'details': ajax})

#When querying a ForeignKey field, you 'normally' pass an instance of the model
#like this for example,
# x = MenCategory.objects.get(men=proname) 
#card_details = MenFashion.objects.filter(category= x).all
#You can however, use __ (double underscore) to 'hop' across and query a specific field.
#card_details = WomenFashion.objects.filter(category__women = proname).all