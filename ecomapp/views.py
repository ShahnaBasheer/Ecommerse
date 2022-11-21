from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from . import models
from itertools import chain
from django.contrib.auth.models import User
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.template.loader import render_to_string
from ecomapp.models import BoysCategory, BoysDetail,BoysFashion, Brand, Cart, CartItem,GirlsCategory, GirlsDetail,GirlsFashion,MenCategory, MenDetail,MenFashion, Seller,WomenCategory,WomenDetail,WomenFashion,Size,KidsAge
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
      if len(discount_list) == 1:
         range_value = (int(discount_list[0]),99)
      else:      
         range_value = (min(list(map(int,discount_list))),99)
      card_details = card_details.filter(discount__range = range_value).all().distinct().order_by('discount')
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
      if len(discount_list) == 1:
         range_value = (int(discount_list[0]),99)
      else:      
         range_value = (min(list(map(int,discount_list))),99)
      card_details = card_details.filter(discount__range = range_value).all().distinct().order_by('discount')
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
       if len(discount_list) == 1:
         range_value = (int(discount_list[0]),99)
       else:      
         range_value = (min(list(map(int,discount_list))),99)
       girls_filt = girls_filt.filter(discount__range = range_value).all().distinct()
       boys_filt = boys_filt.filter(discount__range = range_value).all().distinct()
       card_details = girls_filt.union(boys_filt).order_by('discount')
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
       if len(discount_list) == 1:
          range_value = (int(discount_list[0]),99)
       else:      
          range_value = (min(list(map(int,discount_list))),99)
       card_details = card_details.filter(discount__range = range_value).all().distinct()
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
       if len(discount_list) == 1:
         range_value = (int(discount_list[0]),99)
       else:      
         range_value = (min(list(map(int,discount_list))),99)
       card_details = card_details.filter(discount__range = range_value).all().distinct()
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
    context = {} 
    try:
      if request.user.is_authenticated:
         cartdata = Cart.objects.get(user=request.user)
         cartitem = CartItem.objects.all()
         total_amnt = cartdata.total_amnt + cartdata.total_dscnt
         context = {
           'cart':cartdata,
           'cartitems':cartitem,
           'total':total_amnt,
         }
    except Cart.DoesNotExist:
      context = {
        'cart': 0
      }  
    return render(request,'cart.html',context)

#Not s view function,it is for reusability only
    
def cart_update(cart):
    cart_obj = CartItem.objects.filter(cart=cart)
    if len(cart_obj) == 0:
      cart.delete()
    else:
      cart.total_qty = cart_obj.aggregate(quantity=Sum('quantity'))['quantity']  
      cart.total_amnt = cart_obj.aggregate(total_price=Sum('total_price'))['total_price']
      cart.total_dscnt = cart_obj.aggregate(total_mrp=Sum('total_mrp'))['total_mrp'] - cart.total_amnt
      cart.dlvry_chrg = cart_obj.aggregate(delivery=Sum('delivery'))['delivery']
      cart.save()

@login_required
def add_to_cart(request,product_id):
    products = '';
    infotag = request.GET['info'];
    size = Size.objects.get(size=request.GET['size'])
    seller = Seller.objects.get(seller=request.GET['seller'])
    if request.user.is_authenticated:      
        if infotag == 'women':
            products = WomenFashion.objects.get(pk=product_id) 
        if infotag == 'men':
            products = MenFashion.objects.get(pk=product_id)
        if infotag == 'girls':
            products = GirlsFashion.objects.get(pk=product_id)
        if infotag == 'boys':
            products = BoysFashion.objects.get(pk=product_id) 
      
        cart,created = Cart.objects.get_or_create(user=request.user)
        cartitem,created = products.cartitems.get_or_create(cart=cart,seller=seller,
                       brand=products.brand,cart_image=products.card_image,
                       size=size,title=products.title)  
        if not created:
           cartitem.quantity += 1
        cartitem.save()  
        cart_update(cart)           
    return JsonResponse({'cart_qnty':cart.total_qty})

def update_quantity(request,cart_id):
    cart = Cart.objects.get(user=request.user)
    cartitem = CartItem.objects.get(pk=cart_id)
    cartitem.quantity += 1
    cartitem.save()
    cart_update(cart)
    return redirect('cart')

def delete_quantity(request,cart_id):
    cart = Cart.objects.get(user=request.user)
    cartitem = CartItem.objects.get(pk=cart_id)
    cartitem.quantity -= 1
    if cartitem.quantity == 0:
       cartitem.delete()
       cart_update(cart)
    else:
       cartitem.save()
       cart_update(cart)
    return redirect('cart')

def remove_cart_item(request,cart_id):
    cart = Cart.objects.get(user=request.user)
    cartitem = CartItem.objects.get(pk=cart_id)
    cartitem.delete()
    cart_update(cart)
    return redirect('cart')

#When querying a ForeignKey field, you 'normally' pass an instance of the model
#like this for example,
# x = MenCategory.objects.get(men=proname) 
#card_details = MenFashion.objects.filter(category= x).all
#You can however, use __ (double underscore) to 'hop' across and query a specific field.
#card_details = WomenFashion.objects.filter(category__men = proname).all