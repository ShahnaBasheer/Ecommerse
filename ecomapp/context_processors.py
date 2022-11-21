from .models import Brand, Cart

def quantity(request):
    cart = 0
    try:
       if request.user.is_authenticated:
         cart = Cart.objects.get(user=request.user).total_qty
    except Cart.DoesNotExist:
      cart = 0
    return {'quantity': cart}

def brands(request):
    all_brands = Brand.objects.all().order_by('brand')
    return {'allbrands':all_brands}