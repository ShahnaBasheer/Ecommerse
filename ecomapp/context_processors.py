from itertools import chain
from .models import AllFashion, Brand, Category, Color,EcomCart

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
    category = Category.objects.values_list('category',flat=True).all()
    title = allproducts.values_list('title',flat=True).all()
    brand = Brand.objects.values_list('brand',flat=True).all()
    extras = extras_s = []
    for i in category:
        for x in ['women','men','kids','girls','boys']:
           with_s =  i+" "+"for"+" " +x
           extras.append(with_s) 
        for x in ['women','men','kids','girls','boys']:
           without_s = i[:-1].replace('-'," ")+" "+"for"+" " +x
           extras_s.append(without_s) 
        if '-' in i:
              extras_s.append(i.replace('-',' '))          
    all_items = list(chain(extras,category,title,brand,extras_s))
    return {'automate_search':all_items}