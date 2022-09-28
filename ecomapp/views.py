
from math import prod
from django.shortcuts import render,redirect
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
  card_details1 = GirlsFashion.objects.all()
  card_details2 = BoysFashion.objects.all()
  gproducts = GirlsCategory.objects.all()
  bproducts = BoysCategory.objects.all()
  context = {
    'girls_products':gproducts,
    'boys_products':bproducts,
    'girls_details':card_details1,
    'boys_details':card_details2,
    
  }
  return render(request,'kids.html')

#here, i have create functions for filitering products from database

def womenproducts(request):
    proname = request.POST.get('product')
    card_details = WomenFashion.objects.filter(category__women = proname).all
    context = {
      'allproducts': WomenCategory.objects.all(),
      'details':card_details,
    }
    return render(request,'women.html',context)

#When querying a ForeignKey field, you 'normally' pass an instance of the model
#like this for example,
# x = MenCategory.objects.get(men=proname) 
#card_details = MenFashion.objects.filter(category= x).all

def menproducts(request):
    proname = request.POST.get('product')
    card_details = MenFashion.objects.filter(category__men= proname).all
    context = {
       'allproducts':MenCategory.objects.all(),
       'details':card_details,
    } 
    return render(request,'men.html',context)
    