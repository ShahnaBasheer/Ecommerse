import re
from django.db.models import Count,F
from django.db.models import Q
from .models import CustomUser, EcomCart, EcomCartItem, Seller_Product, SaveForLater
from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from . import import_fnctns as fncs,context_processors
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from ecommapp.models import AllFashion,Color
# Create your views here.

def signin(request):
    if request.method == 'POST':
      username = request.POST['username']
      password = request.POST['password']  
      user = authenticate(username=username, password=password)
      if user is not None:
        login(request,user)
        fname = user.first_name
        messages.success(request, "you are logged in successfully")
        return render(request,'homepage.html',{'fname': fname})
      else:
        messages.error(request, "Invalid Credentials!")
        return redirect('signin')  
    return render(request,'login.html')
    
def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!")
    return redirect('homepage') 

def home(request):
    return render(request,'homepage.html')

def registration(request):
    if request.method == "POST":
        #username = request.POST.get('username')
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        gender = request.POST['gender']
        dob = request.POST['birthdate']
        telephone = request.POST['telephone']
        password = request.POST['password']
        repeatpass = request.POST['repeatpassword']
        myuser = CustomUser.objects.create_user(username,email,password)
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.phone_no = telephone
        myuser.dob = dob
        myuser.gender = gender
        myuser.save() 
        messages.success(request,"your Account has been successfully created.")
        return redirect('signin')
    return render(request,'registration.html')

def womentab(request):
    card_details = AllFashion.objects.filter(gender="women").all()
    context = fncs.product_page(card_details,"women")
    return render(request,'women.html',context)

def mentab(request):
    card_details = AllFashion.objects.filter(gender="men").all()
    context = fncs.product_page(card_details,"men")
    return render(request,'men.html',context)

def kidstab(request):
    card_details = AllFashion.objects.filter(Q(gender='girls') | Q(gender='boys')).all()
    kids_age = card_details.values(pro=F('age__age')).annotate(count=Count('age'))
    context = fncs.product_page(card_details,"kids")
    context['allproducts']['age'] = kids_age
    return render(request,'kids.html',context)

def filter_women(request):
    card_details = AllFashion.objects.filter(gender="women").all()
    context = fncs.product_filters(card_details,request,'women')
    return JsonResponse(context)

def filter_men(request):
    card_details = AllFashion.objects.filter(gender="men").all()
    context = fncs.product_filters(card_details,request,'men') 
    return JsonResponse(context)

def filter_kids(request):
    card_details = AllFashion.objects.filter(Q(gender='girls') | Q(gender='boys')).all()
    context = fncs.product_filters(card_details,request,'kids')
    return JsonResponse(context)

def product_info(request,slug):
    gotocart = p = selected_s = f = False
    products = AllFashion.objects.get(slug=slug)   
    all_sizes =  AllFashion.objects.filter(slug=slug).values_list('Sellers__size__sizes',flat=True).\
         exclude(Sellers__size__sizes='Free Size').distinct()
    q = products.Sellers.all()[0]
    seller_s = q.seller
    if 'sl' in request.GET:
        q = products.Sellers.get(seller__seller=request.GET['sl'])
        ajax = render_to_string("size-selected.html",{'seller_s':q.seller.seller,'details':products,
        'sizeall':all_sizes,'not_size':[i for i in q.size.values_list('sizes',flat=True)]})
        return JsonResponse({'sizes':ajax})                
    if 'size' in request.GET and 'seller' in request.GET:
        f = True
        m = products.Sellers.get(seller__seller=request.GET['seller'])
        p = m.size.get(sizes=request.GET['size'])
        seller_s = request.GET['seller']
        selected_s = request.GET['size']           
    if request.user.is_authenticated:
        try:
            cartdata = EcomCart.objects.get(user=request.user)
            cartitem = EcomCartItem.objects.filter(cart=cartdata,size=p if f  else q.specifications ,
                       carted_product=products,seller=q)
        except EcomCart.DoesNotExist:
            cartdata = cartitem = []   
        if len(cartitem) > 0:
            gotocart = True  
    context = {
      'details':products,      
      'sizeall':all_sizes,
      'q':False if(f) else q,
      's':p,
      'not_size':[i for i in m.size.values_list('sizes',flat=True)]
                 if(f) else [i for i in q.size.values_list('sizes',flat=True)],
      'seller_s':seller_s,
      'selected_s':selected_s,
      'gotocart':gotocart,
    }  
    return render(request,'product-info.html',context)

def cart(request):
    context = {} 
    if request.user.is_authenticated:
       save_for_later = SaveForLater.objects.filter(user=request.user)
       try:
          cartdata = EcomCart.objects.get(user=request.user)
          cartitem = EcomCartItem.objects.filter(cart=cartdata)
          total_amnt = cartdata.total_amnt + cartdata.total_dscnt
          context = {
            'cart':cartdata,
            'cartitems':cartitem,
            'total':total_amnt,
            'saveit':save_for_later,
          }
       except EcomCart.DoesNotExist:
         context = {
           'cart': 0,
           'saveit':save_for_later,
         }  
    return render(request,'cart.html',context)
    

@login_required
def add_to_cart(request,product_id):
    products = seller = size = '';
    if request.user.is_authenticated:
        products = AllFashion.objects.get(pk=product_id)  
        seller = products.Sellers.get(seller__seller = request.GET['seller'])
        size = seller.size.get(sizes = request.GET['size'])
 
        cart,created = EcomCart.objects.get_or_create(user=request.user)
        cartitem,created = products.cartitems.get_or_create(cart=cart,seller=seller,
                       brand=products.brand,cart_image=products.card_image,
                       size=size,title=products.title)  
        if not created:
           cartitem.quantity += 1 
        cartitem.save()  
        fncs.cart_update(cart)
        saveit = SaveForLater.objects.filter(user=request.user,image=products.card_image,
                size=size,seller=seller,brand=products.brand,title=products.title)
        saveit.delete()               
    return JsonResponse({'cart_qnty':cart.total_qty ,'product': product_id})

def update_quantity(request,cart_id):
    cart = EcomCart.objects.get(user=request.user)
    cartitem = EcomCartItem.objects.get(pk=cart_id)
    cartitem.quantity += 1
    cartitem.save()
    fncs.cart_update(cart)
    return redirect('cart')

def delete_quantity(request,cart_id):
    cart = EcomCart.objects.get(user=request.user)
    cartitem = EcomCartItem.objects.get(pk=cart_id)
    cartitem.quantity -= 1
    if cartitem.quantity == 0:
       cartitem.delete()
       fncs.cart_update(cart)
    else:
       cartitem.save()
       fncs.cart_update(cart)
    return redirect('cart')

def remove_cart_item(request,cart_id):
    cart = EcomCart.objects.get(user=request.user)
    cartitem = EcomCartItem.objects.get(pk=cart_id)
    cartitem.delete()
    fncs.cart_update(cart)
    return redirect('cart')

def save_for_later(request,save_id):
    cart = EcomCart.objects.get(user=request.user)
    carteditem = EcomCartItem.objects.get(pk = save_id)
    save_later = SaveForLater(user=request.user,image=carteditem.cart_image,
        title=carteditem.title,brand=carteditem.brand,size=carteditem.size,
        seller=carteditem.seller,qty=carteditem.quantity,all_pro=carteditem.carted_product)
    save_later.save() 
    carteditem.delete()
    fncs.cart_update(cart)
    return redirect('cart')

def remove_save_later(request,save_id):
    save_later = SaveForLater.objects.get(pk=save_id)
    save_later.delete()
    return redirect('cart')

def move_to_cart(request,move_id):
    saveit = SaveForLater.objects.get(pk=move_id)
    cart,created = EcomCart.objects.get_or_create(user=request.user)
    cartitem,created = EcomCartItem.objects.get_or_create(cart=cart,
        cart_image=saveit.image,size=saveit.size,
        title=saveit.title,brand=saveit.brand,total_mrp=saveit.size.mrp,
        seller=saveit.seller,total_price=saveit.size.price, 
        quantity=saveit.qty,carted_product=saveit.all_pro)
    cartitem.save()
    saveit.delete()
    fncs.cart_update(cart)
    return redirect('cart')

def searchall(request):  
    search = request.GET['search'].lower().strip()
    searchType = request.GET['searchType']           
    card_details = fncs.searchbar(request,search,searchType)
    context = fncs.product_page(card_details['details'],request,'')
    context['search'] = search
    context['search_Type'] = searchType
    return render(request,'search-page.html',context)

def filter_search(request):
    search = request.GET['search'].lower().strip()
    searchType = request.GET['searchType'] 
    card_details = fncs.searchbar(request,search,searchType)
    context = fncs.product_filters(card_details['details'],request,'')
    return JsonResponse(context)

def all_brands(request):
    brand_search = request.GET['brand']
    card_details = AllFashion.objects.filter(brand__brand = brand_search).all()
    context = fncs.product_page(card_details,'')
    context['allproducts'].pop('brand')
    context['search'] = brand_search
    return render(request,"brands.html",context)

def filter_brands(request):
    brand_search = request.GET['slct_brand']
    card_details = AllFashion.objects.filter(brand__brand=brand_search).all()
    context = fncs.product_filters(card_details,request,'')  
    return JsonResponse(context)
#When querying a ForeignKey field, you 'normally' pass an instance of the model
#like this for example,
# x = MenCategory.objects.get(men=proname) 
#card_details = MenFashion.objects.filter(category= x).all
#You can however, use __ (double underscore) to 'hop' across and query a specific field.
#card_details = WomenFashion.objects.filter(category__men = proname).all