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
from ecomapp.models import BoysCategory, BoysDetail,BoysFashion, Brand, Cart, CartItem,GirlsCategory, GirlsDetail,GirlsFashion,MenCategory, MenDetail,MenFashion, SaveItForLater, Seller,WomenCategory,WomenDetail,WomenFashion,Size,KidsAge
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
    brand = Brand.objects.all()
    discounts = models.DISCOUNT_CHOICES
    #g_count = WomenFashion.objects.values('category__women').annotate(count = Count('id'))
    context = {
      'allproducts':{'category':products,'size':size,'discounts':discounts,'brands':brand},
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

def sortby(*args):
    if args[1] == ['price_asc']:
        card_details = args[0].order_by('price')
    elif args[1] == ['price_desc']:
        card_details = args[0].order_by('-price')
    elif args[1] == ['newest']:
        card_details = args[0].order_by('-upload_date')
    elif args[1] == ['disc_desc']:
        card_details = args[0].order_by('-discount')
    elif args[1] == ['delivery']:
        if len(args) == 4:
          girls_filt = args[2].filter(dlvry_charges = "FREE")
          boys_filt = args[3].filter(dlvry_charges = "FREE")
          card_details = girls_filt.union(boys_filt)
        else:
          card_details = args[0].filter(dlvry_charges = "FREE").all().distinct()
    else:
        card_details = args[0]
    print(args[1])
    print(len(args))
    print(card_details)
    return card_details

def filter_women(request):
    card_details = WomenFashion.objects.all()
    pro_list = request.GET.getlist('category[]')
    size_list = request.GET.getlist('size[]')
    discount_list = request.GET.getlist('discount[]')
    sort_data = request.GET.getlist('sort[]')
    if len(pro_list) > 0:
      card_details = card_details.filter(category__women__in = pro_list).all().distinct()
    if len(size_list) > 0:
      card_details = card_details.filter(size__size__in = size_list).all().distinct()
    if len(discount_list) > 0:
      if len(discount_list) == 1:
         range_value = (int(discount_list[0]),99)
      else:      
         range_value = (min(list(map(int,discount_list))),99)
      card_details = card_details.filter(discount__range = range_value).all().distinct()
    card_details = sortby(card_details,sort_data)
    #add __in columnname to filter list of values    
    #add getlist to take values as list      
    ajax = render_to_string('cards.html', {'details': card_details})
    return JsonResponse({'details': ajax})

def filter_men(request):
    card_details = MenFashion.objects.all()
    pro_list = request.GET.getlist('category[]')
    size_list = request.GET.getlist('size[]')
    discount_list = request.GET.getlist('discount[]')
    sort_data = request.GET.getlist('sort[]')
    if len(pro_list) > 0:
      card_details = card_details.filter(category__men__in = pro_list).all().distinct() 
    if len(size_list) > 0:
      card_details = card_details.filter(size__size__in = size_list).all() .distinct()      
    if len(discount_list) > 0:
      if len(discount_list) == 1:
         range_value = (int(discount_list[0]),99)
      else:      
         range_value = (min(list(map(int,discount_list))),99)
      card_details = card_details.filter(discount__range = range_value).all().distinct()
    card_details = sortby(card_details,sort_data)
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
    sort_data = request.GET.getlist('sort[]')
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
       card_details = girls_filt.union(boys_filt)
    card_details = sortby(card_details,sort_data,girls_filt,boys_filt)
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
    sort_data = request.GET.getlist('sort[]')
    print("****************")
    print(age_list)
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
    card_details = sortby(card_details,sort_data)
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
    sort_data = request.GET.getlist('sort[]')
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
    card_details = sortby(card_details,sort_data)
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
    if request.user.is_authenticated:
       save_for_later = SaveItForLater.objects.filter(user=request.user)
       try:
          cartdata = Cart.objects.get(user=request.user)
          cartitem = CartItem.objects.filter(cart=cartdata)
          total_amnt = cartdata.total_amnt + cartdata.total_dscnt
          context = {
            'cart':cartdata,
            'cartitems':cartitem,
            'total':total_amnt,
            'saveit':save_for_later,
          }
       except Cart.DoesNotExist:
         context = {
           'cart': 0,
           'saveit':save_for_later,
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
        saveit = SaveItForLater.objects.filter(user=request.user,image=products.card_image,
                size=size,seller=seller,brand=products.brand,title=products.title)
        if saveit:
           saveit.delete()                   
    return JsonResponse({'cart_qnty':cart.total_qty,'product':product_id,'info':infotag})

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

def save_for_later(request,save_id):
    cart = Cart.objects.get(user=request.user)
    cartitem =  CartItem.objects.get(pk = save_id)
    save_later = SaveItForLater(user=request.user,image=cartitem.cart_image,
        title=cartitem.title,brand=cartitem.brand,size=cartitem.size,
        seller=cartitem.seller,price=cartitem.total_price,mrp=cartitem.total_mrp,
        qty=cartitem.quantity,object_id=cartitem.object_id,
        content_type_id=cartitem.content_type_id)
    save_later.save() 
    cartitem.delete()
    cart_update(cart)
    return redirect('cart')

def remove_save_later(request,save_id):
    save_later = SaveItForLater.objects.get(pk=save_id)
    save_later.delete()
    return redirect('cart')

def move_to_cart(request,move_id):
    saveit = SaveItForLater.objects.get(pk=move_id)
    cart,created = Cart.objects.get_or_create(user=request.user)
    cartitem,created = CartItem.objects.get_or_create(cart=cart,
        cart_image=saveit.image,size=saveit.size,
        title=saveit.title,brand=saveit.brand,total_mrp=saveit.mrp,
        seller=saveit.seller,total_price=saveit.price, 
        quantity=saveit.qty,object_id=saveit.object_id,
        content_type_id=saveit.content_type_id)
    cartitem.save()
    saveit.delete()
    cart_update(cart)
    return redirect('cart')

#When querying a ForeignKey field, you 'normally' pass an instance of the model
#like this for example,
# x = MenCategory.objects.get(men=proname) 
#card_details = MenFashion.objects.filter(category= x).all
#You can however, use __ (double underscore) to 'hop' across and query a specific field.
#card_details = WomenFashion.objects.filter(category__men = proname).all