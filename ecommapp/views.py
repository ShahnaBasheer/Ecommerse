
from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string
from .forms import RegistrationForm
from django.db.models import Count,F
from django.db.models import Q
from .models import Brand, CustomUser, EcomCart, EcomCartItem, KidsAge, ProductInfo, Seller, Seller_Product, SaveForLater, Size
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from . import import_fnctns as fncs
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from ecommapp.models import AllFashion,Color

from ecommapp import models
# Create your views here.


def selleradd(request):
    products = AllFashion.objects.all()
    proinfo = ProductInfo.objects.all()
    brands = Brand.objects.all()
    ages = KidsAge.objects.all()
    colors = Color.objects.all()
    sellers = Seller.objects.all()
     
    if request.method == 'POST':
        bran = request.POST.get('bran')
        b_about = request.POST.get('aboutbrand')
        cat = request.POST.get('category')
        gender = request.POST.get('gender') 
        age = request.POST.getlist('age')    
        title = request.POST.get('title')    
        material = request.POST.get('material')    
        pattern = request.POST.get('pattern')    
        pocket = request.POST.get('pocket')    
        sleeves = request.POST.get('sleeves')    
        neck = request.POST.get('neck')    
        occasion = request.POST.get('occasion')    
        package = request.POST.get('package')
        rise = request.POST.get('rise')    
        care = request.POST.get('care')    
        description = request.POST.get('description')    
        country = request.POST.get('country')
        manufacture = request.POST.get('manufacture')
        sell = request.POST.get('sell')
        img = request.POST.get('img')
        s = request.POST.get('S')
        xs = request.POST.get('XS')
        m = request.POST.get('M')
        l = request.POST.get('L')
        xl = request.POST.get('XL')
        xl2 = request.POST.get('2XL')
        xl3 = request.POST.get('3XL')
        xl4 = request.POST.get('4XL')
        freesize = request.POST.get('fs')
        brnd =request.POST.get('brnd')      
        deliv = request.POST.get('deli')
        speci = request.POST.get('speci') 
        retu = request.POST.get('return')  
        color = request.POST.getlist('color[]')
        clr = request.POST.getlist('colors[]')
        stretch = request.POST.get('Stretchable')
        rr = [i for i in [s,xs,m,l,xl,xl2,xl3,xl4,freesize] if i!=None]
          
        if 'seller' in request.POST and 'sellerabout':
            seller = request.POST.get('seller')
            s_about = request.POST.get('sellerabout')
            s_details,created = Seller.objects.get_or_create(seller=seller,about_us=s_about)
            s_details.save()

        br = brands.get(brand=brnd)
        if 'title' in request.POST:
            if brnd == False:
                br = brands.create(brand=bran,about=b_about) 
            br.save()         
            
            procs = products.create(gender=gender,title=title,brand=br,
                        category=cat,card_image=img)
            produinfo = proinfo.create(Material=material,
                        Pattern=pattern,Pocket=pocket,Sleeves=sleeves,Neck=neck,
                        Packet_Contains=package,Occasion=occasion,Rise=rise,
                        Stretchable=stretch,Care_instructions=care,Descriptions=description,
                        Country=country,Manufacture=manufacture)
            procs.Products = produinfo
            
            clrs = color
            if clr != []:    
              clrs = clr
            for f in clrs:
               colr = colors.get_or_create(color=f)
               produinfo.Color.set([colr])
               colr.save()      


            for q in age:
               kids_age = ages.get(age=q)   
               procs.age.set([kids_age])      
            sp = sellers.get(seller=sell)                        
            pks = procs.Sellers.create(seller=sp,Return=retu,dlvry_charges=deliv)

            for i in rr:
                v = int(request.POST.get(i+"_price"))
                b = int(request.POST.get(i+"_mrp"))
                n = int(request.POST.get(i+"_stock"))
                if i == 'fs':
                  i = 'Free Size'
                s = Size.objects.create(sizes=i,price=v,mrp=b,stock=n)
                s.save()
                pks.size.add(s.id)
                if i == speci:
                   pks.specifications = s 
                pks.save()    
            br.save()          
            produinfo.save()
            procs.Sellers.add(pks.id)    
            procs.save()
            
    context = {
        'details':products,
        'seller':sellers,
        'ages':ages,
        'brands':brands,
        'colors':colors,
    }        

    return render(request,"seller.html",context)

def signin(request):
    if request.method == 'POST':
      username = request.POST['username']
      password = request.POST['password'] 
      user = authenticate(username=username, password=password)
      if user is not None:
        login(request,user)
        fname = user.first_name
        messages.success(request,"Helloo "+username+", you are logged in successfully")
        status = 200
        return JsonResponse({'status':status})
      else:
        ajax = "Invalid Credentials!"
        status = 400   
        return JsonResponse({'login':ajax,'status':status}) 
    return redirect('homepage')
   
def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!")
    return redirect('homepage') 

def home(request):
    return render(request,'homepage.html')

def registration(request):
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)   
        if form.is_valid():
           if CustomUser.objects.filter(email=request.POST['email']).exists():
              messages.error(request,"User with that email already exists")
              return redirect('registration')
           else: 
              user = form.save(commit=False)
              user.set_password(form.cleaned_data['password'])
              user.save()
              messages.success(request,"your Account has been successfully created.\
                     please Login.")
              return redirect('login') 
        else:
            messages.error(request,"User with that username already exists")     
            return redirect('registration')    
    context = {
       'form':form,
    }    
    return render(request,'registration.html',context)
def profile(request):
    profile = CustomUser.objects.get(username=request.user) 
    return render(request,'profile-page.html',{'profile':profile})

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