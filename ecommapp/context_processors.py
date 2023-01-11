from itertools import chain
from .models import AllFashion, Brand, EcomCart
from django.db.models import Q

def quantity(request):
    cart = 0
    try:
       if request.user.is_authenticated:
         cart = EcomCart.objects.get(user=request.user).total_qty
    except EcomCart.DoesNotExist:
      cart = 0
    return {'quantity': cart}

def brands(request):
    all_brands = Brand.objects.all().order_by('brand')
    return {'allbrands':all_brands}
  
def search_items(request):
    allproducts = AllFashion.objects.all()
    category = allproducts.values_list('category',flat=True).all()
    title = allproducts.values_list('title',flat=True).all()
    brand = Brand.objects.values_list('brand',flat=True).all()
    f = []
    def hello(gender):
      q = allproducts.filter(gender=gender).all().\
         values_list('category',flat=True).distinct()
      if gender == 'kids':
        q = allproducts.filter(Q(gender='girls')|Q(gender='boys')).all().\
           values_list('category',flat=True).distinct()
       
      for i in q:
        with_s =  i+" "+"for"+" " +gender
        #without_s = i[:-1].replace('-'," ")+" "+"for"+" " +gender
        f.append(with_s)
    p = ['men','women','boys','girls','kids']    
    for i in p: hello(i)  
    all_items = list(chain(category,brand,f,title))
    return {'automate_search':all_items}