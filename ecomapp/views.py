from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from . import import_fnctns
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from ecomapp.models import Cart, CartItem, KidsCategory, KidsDetail, KidsFashion, MenCategory, MenDetail,MenFashion, Pocket, ProductDetail, SaveItForLater, Seller,WomenCategory,WomenDetail,WomenFashion,Size,KidsAge
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
    pro_info = WomenDetail.objects.all()
    context = import_fnctns.product_page(card_details,pro_info,'women')
    return render(request,'women.html',context)

def mentab(request):
    card_details = MenFashion.objects.all()
    pro_info = MenDetail.objects.all()
    context = import_fnctns.product_page(card_details,pro_info,'men')
    return render(request,'men.html',context)

def kidstab(request):
    card_details = KidsFashion.objects.all()
    pro_info = KidsDetail.objects.all()
    kids_age = KidsAge.objects.all()
    context = import_fnctns.product_page(card_details,pro_info,'kids')
    context['allproducts']['age'] = kids_age
    return render(request,'kids.html',context)

def filter_women(request):
    card_details = WomenFashion.objects.all()
    context = import_fnctns.product_filters(card_details,request,'women')
    return JsonResponse(context)

def filter_men(request):
    card_details = MenFashion.objects.all()
    context = import_fnctns.product_filters(card_details,request,'men') 
    return JsonResponse(context)

def filter_kids(request):
    card_details = KidsFashion.objects.all()
    context = import_fnctns.product_filters(card_details,request,'kids')
    return JsonResponse(context)

def product_info(request,product_id):
    products = ""
    product_details= ""
    gotocart = sizeall = False
    infotag = request.GET['info']
    if infotag == 'women':
       products = WomenFashion.objects.get(pk = product_id)
       product_details = get_object_or_404(WomenDetail, Product__id = product_id)         
    if infotag =='men':
       products = MenFashion.objects.get(pk = product_id)
       product_details = get_object_or_404(MenDetail, Product__id = product_id)
    if infotag == 'kids':
       products = KidsFashion.objects.get(pk = product_id)
       product_details = get_object_or_404(KidsDetail, Product__id = product_id)
    if request.user.is_authenticated:
        cartdata = Cart.objects.get(user=request.user)
        cartitem = CartItem.objects.filter(cart=cartdata).values_list('title',flat=True).distinct()
        if products.title in cartitem:
            gotocart = True      
    if len(products.size.all()) > 0:
        sizeall = True
    context = {
      'details':products,
      'gender':infotag,
      'productdetails':product_details,
      'gotocart':gotocart,
      'sizeall':sizeall,   
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
        if infotag == 'kids':
            products = KidsFashion.objects.get(pk=product_id)
      
        cart,created = Cart.objects.get_or_create(user=request.user)
        cartitem,created = products.cartitems.get_or_create(cart=cart,seller=seller,
                       brand=products.brand,cart_image=products.card_image,
                       size=size,title=products.title)  
        if not created:
           cartitem.quantity += 1
        cartitem.save()  
        import_fnctns.cart_update(cart)
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
    import_fnctns.cart_update(cart)
    return redirect('cart')

def delete_quantity(request,cart_id):
    cart = Cart.objects.get(user=request.user)
    cartitem = CartItem.objects.get(pk=cart_id)
    cartitem.quantity -= 1
    if cartitem.quantity == 0:
       cartitem.delete()
       import_fnctns.cart_update(cart)
    else:
       cartitem.save()
       import_fnctns.cart_update(cart)
    return redirect('cart')

def remove_cart_item(request,cart_id):
    cart = Cart.objects.get(user=request.user)
    cartitem = CartItem.objects.get(pk=cart_id)
    cartitem.delete()
    import_fnctns.cart_update(cart)
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
    import_fnctns.cart_update(cart)
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
    import_fnctns.cart_update(cart)
    return redirect('cart')

#When querying a ForeignKey field, you 'normally' pass an instance of the model
#like this for example,
# x = MenCategory.objects.get(men=proname) 
#card_details = MenFashion.objects.filter(category= x).all
#You can however, use __ (double underscore) to 'hop' across and query a specific field.
#card_details = WomenFashion.objects.filter(category__men = proname).all