from itertools import chain
import re
from django.db.models import Count,F
from django.db.models import Q
from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from . import import_fnctns as fncs,context_processors
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from ecomapp.models import AllFashion, Category, Color, EcomCart, EcomCartItem,Pocket, ProductInfo, SaveForLater,Seller,Size,KidsAge, Sleeve
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
      password = request.POST['password']
      repeatpass = request.POST['repeatpass']
      myuser = User.objects.create_user(username,email,password)
      myuser.first_name = firstname
      myuser.last_name = lastname
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
    gotocart = sizeall = False
    products = AllFashion.objects.get(slug=slug)   
    product_details = get_object_or_404(ProductInfo, Product__slug = slug)         
    if request.user.is_authenticated:
        try:
            cartdata = EcomCart.objects.get(user=request.user)
            cartitem =  EcomCartItem.objects.filter(cart=cartdata).values_list('title',flat=True).distinct()
        except EcomCart.DoesNotExist:
            cartdata = cartitem = []   
        if products.title in cartitem:
            gotocart = True      
    if len(products.size.all()) > 0:
        sizeall = True
    context = {
      'details':products,
      'productdetails':product_details,
      'gotocart':gotocart,
      'sizeall':sizeall,   
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
    products = '';
    seller = Seller.objects.get(seller=request.GET['seller'])
    if "size" in request.GET:
        size = Size.objects.get(size=request.GET['size'])
    else:
        size = None
    if request.user.is_authenticated:      
        products = AllFashion.objects.get(pk=product_id)   
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
        if saveit:
           saveit.delete()                   
    return JsonResponse({'cart_qnty':cart.total_qty,'product':product_id})

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
    cartitem = EcomCartItem.objects.get(pk = save_id)
    save_later = SaveForLater(user=request.user,image=cartitem.cart_image,
        title=cartitem.title,brand=cartitem.brand,size=cartitem.size,
        seller=cartitem.seller,price=cartitem.total_price,mrp=cartitem.total_mrp,
        qty=cartitem.quantity,all_pro=cartitem.products,)
    save_later.save() 
    cartitem.delete()
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
        title=saveit.title,brand=saveit.brand,total_mrp=saveit.mrp,
        seller=saveit.seller,total_price=saveit.price, 
        quantity=saveit.qty,products=saveit.all_pro)
    cartitem.save()
    saveit.delete()
    fncs.cart_update(cart)
    return redirect('cart')

def searchall(request):
    search = request.GET['search'].lower().strip()
    searchType = request.GET['searchType']
    allproducts = AllFashion.objects.all()
    card_details = False
    color = list(Color.objects.values_list('color',flat=True).all())
    auto_items = context_processors.search_items(request)['automate_search'] + color                
    auto_items = [items.lower() for items in auto_items] 
    category = list(Category.objects.values_list('category',flat=True).all())
    cat_nospace =[i.lower().replace('-','').replace(' ','') for i in category]
    for_items = ["women","men","girls","boys","kids"]
    split_s = search.split('for')
    split_s = [i.strip() for i in split_s]   
    cat = fncs.checker(cat_nospace,split_s,category)  
    
    if searchType == 'AutomateSearch':    
        if len(split_s) == 2 and any(i in split_s for i in for_items):  
            card_details = allproducts.filter(Q(category__category__istartswith=cat) & 
                           fncs.gender_checker(split_s[1])).all().distinct()
            
        else:
            card_details = allproducts.filter(Q(category__category__istartswith=search)|
                         Q(title__iexact=search)|Q(brand__brand__iexact=search)).all().distinct()   
    
    elif searchType == 'ManualSearch':
        if any([search == x for x in auto_items]):
            if len(split_s) == 2 and any(i in split_s for i in for_items):
                card_details = allproducts.filter(Q(category__category__istartswith=cat) & 
                           fncs.gender_checker(split_s[1])).all().distinct()
                
            else:
                card_details = allproducts.filter(Q(category__category__istartswith=search)|
                             Q(title__istartswith=search)|Q(brand__brand__iexact=search)|
                             Q(pros__Color__color__icontains=search)).all().distinct()
                  
        elif len(search.split()) > 1 :    
            if re.search(' t shirt|t-shirt|t shirt',search) :
               search = search.replace('t shirt',' tshirt').replace('t-shirt',' tshirt')
               split_s = search.split()
            else:   
               split_s = search.split() 
            split_s = [i.strip() for i in split_s]
            sleeves = list(Sleeve.objects.values_list('sleeves',flat=True).all())
            sleev_nospace = [i.lower().replace('-','').replace(' ','') for i in sleeves]
            sleeve = fncs.checker(sleev_nospace,split_s,sleeves)
            cat =  fncs.checker(cat_nospace,split_s,category)                  
            qs = [Q(pros__Color__color__icontains=i)|Q(brand__brand__iexact=i)for i in split_s] 
            query = qs.pop()
            for q in qs:
                query |= q   
            if len(allproducts.filter(query).all()) == 0:
                query = Q(pros__Sleeves__sleeves__icontains=sleeve)
                card_details = allproducts.filter(query & Q(category__category__istartswith=cat) &
                 fncs.gender_checker(split_s)).all().distinct()
            else:
                card_details = allproducts.filter(query & Q(category__category__istartswith=cat) &
                 fncs.gender_checker(split_s)).all().distinct()
             
    if card_details == False: 
        if re.search(' t shirt|t-shirt|t shirt|tshirt',search) :
            search = search.replace('t shirt','t-shirt').replace('tshirt','t-shirt') 
        card_details = allproducts.filter(Q(category__category__istartswith=search)|
                  Q (pros__Color__color__icontains=search)|Q(brand__brand__contains=search)|
                  Q (pros__Sleeves__sleeves__icontains=search[0:3])|Q(title__istartswith=search)|
                  Q (gender__istartswith=search)).all().distinct()
                
    elif len(card_details) == 0:
        card_details = allproducts.filter(Q(title__icontains=search))
                
    context = fncs.product_page(card_details,'')
    context['search'] = search
    context['search_Type'] = searchType
    return render(request,'search-page.html',context)

def filter_search(request):
    search = request.GET['search'].lower().strip()
    searchType = request.GET['searchType']
    allproducts = AllFashion.objects.all()
    card_details = False
    color = list(Color.objects.values_list('color',flat=True).all())
    auto_items = context_processors.search_items(request)['automate_search'] + color                
    auto_items = [items.lower() for items in auto_items] 
    category = list(Category.objects.values_list('category',flat=True).all())
    cat_nospace =[i.lower().replace('-','').replace(' ','') for i in category]
    for_items = ["women","men","girls","boys","kids"]
    split_s = search.split('for')
    split_s = [i.strip() for i in split_s]   
    cat = fncs.checker(cat_nospace,split_s,category)  
    
    if searchType == 'AutomateSearch':    
        if len(split_s) == 2 and any(i in split_s for i in for_items):  
            card_details = allproducts.filter(Q(category__category__istartswith=cat) & 
                           fncs.gender_checker(split_s[1])).all().distinct()
            
        else:
            card_details = allproducts.filter(Q(category__category__istartswith=search)|
                         Q(title__iexact=search)|Q(brand__brand__iexact=search)).all().distinct()   
    
    elif searchType == 'ManualSearch':
        if any([search == x for x in auto_items]):
            if len(split_s) == 2 and any(i in split_s for i in for_items):
                card_details = allproducts.filter(Q(category__category__istartswith=cat) & 
                           fncs.gender_checker(split_s[1])).all().distinct()
                
            else:
                card_details = allproducts.filter(Q(category__category__istartswith=search)|
                             Q(title__istartswith=search)|Q(brand__brand__iexact=search)|
                             Q(pros__Color__color__icontains=search)).all().distinct()
                  
        elif len(search.split()) > 1 :    
            if re.search(' t shirt|t-shirt|t shirt',search) :
               search = search.replace('t shirt',' tshirt').replace('t-shirt',' tshirt')
               split_s = search.split()
            else:   
               split_s = search.split() 
            split_s = [i.strip() for i in split_s]
            sleeves = list(Sleeve.objects.values_list('sleeves',flat=True).all())
            sleev_nospace = [i.lower().replace('-','').replace(' ','') for i in sleeves]
            sleeve = fncs.checker(sleev_nospace,split_s,sleeves)
            cat =  fncs.checker(cat_nospace,split_s,category)                  
            qs = [Q(pros__Color__color__icontains=i)|Q(brand__brand__iexact=i)for i in split_s] 
            query = qs.pop()
            for q in qs:
                query |= q   
            if len(allproducts.filter(query).all()) == 0:
                query = Q(pros__Sleeves__sleeves__icontains=sleeve)
                card_details = allproducts.filter(query & Q(category__category__istartswith=cat) &
                 fncs.gender_checker(split_s)).all().distinct()
            else:
                card_details = allproducts.filter(query & Q(category__category__istartswith=cat) &
                 fncs.gender_checker(split_s)).all().distinct()
             
    if card_details == False: 
        if re.search(' t shirt|t-shirt|t shirt|tshirt',search) :
            searchs = search.replace('t shirt','t-shirt').replace('tshirt','t-shirt') 
        card_details = allproducts.filter(Q(category__category__istartswith=searchs)|
                  Q (pros__Color__color__icontains=searchs)|Q(brand__brand__contains=search)|
                  Q (pros__Sleeves__sleeves__icontains=searchs[0:3])|Q(title__istartswith=searchs)|
                  Q (gender__istartswith=searchs)).all().distinct()
                
    elif len(card_details) == 0:
        card_details = allproducts.filter(Q(title__icontains=search))
    context = fncs.product_filters(card_details,request,'')
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
