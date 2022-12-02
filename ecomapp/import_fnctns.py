from . import models
from .models import CartItem
from django.db.models import Sum
from django.template.loader import render_to_string

def product_page(*args):
    size = args[0].values_list('size__size',flat=True).exclude(size__size=None).distinct().order_by('-size__id')
    brand = args[0].values_list('brand__brand',flat=True).exclude(brand__brand=None).distinct()
    color = args[1].values_list('Color__color',flat=True).exclude(Color__color=None).distinct()
    material =args[1].values_list('Material__material',flat=True).exclude(Material__material=None).distinct()
    pattern = args[1].values_list('Pattern__pattern',flat=True).exclude(Pattern__pattern=None).distinct()
    occasion = args[1].values_list('Occasion__occasion',flat=True).exclude(Occasion__occasion=None).distinct()
    discounts = models.DISCOUNT_CHOICES
    neck = pocket = sleeve = rise = stretch = [] 
    products = args[0].values_list('category__category',flat=True)\
               .exclude(category__category=None).distinct()
    #g_count = WomenFashion.objects.values('category__women').annotate(count = Count('id'))
    context = {
      'allproducts':{'category':products,'age':None,'brand':brand,'discount':discounts,
                   'size':size,'color':color,'material':material,'pattern':pattern,
                   'occasion':occasion,'neck':neck,'pocket':pocket,'sleeve':sleeve,
                   'rise':rise,'stretchable':stretch},
      'details':args[0],
      'gender':args[2],
    }
    return context

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
        card_details = args[0].filter(dlvry_charges = "FREE").all().distinct()
    else:
        card_details = args[0]
    return card_details

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

def product_filters(*args):
    card_details = args[0]
    gender = args[1].GET.getlist('gender[]')
    age_list = args[1].GET.getlist('age[]')
    size_list = args[1].GET.getlist('size[]')
    discount_list = args[1].GET.getlist('discount[]')
    brand_list = args[1].GET.getlist('brand[]')
    color_list = args[1].GET.getlist('color[]')
    material_list = args[1].GET.getlist('material[]')
    pattern_list = args[1].GET.getlist('pattern[]')
    occasion_list = args[1].GET.getlist('occasion[]')
    neck_list = args[1].GET.getlist('neck[]')
    pocket_list = args[1].GET.getlist('pocket[]')
    sleeve_list = args[1].GET.getlist('sleeve[]')
    rise_list = args[1].GET.getlist('rise[]')
    stretch_list = args[1].GET.getlist('strechable[]')
    sort_data = args[1].GET.getlist('sort[]') 
    cat_list = args[1].GET.getlist('category[]')
    neck = pocket = sleeve = rise = stretch = []
    if len(gender) > 0:
       card_details = card_details.filter(gender__in = gender).all().distinct()
    if len(cat_list) > 0:
       card_details = card_details.filter(category__category__in = cat_list).all().distinct()
       if len(neck_list) > 0:
          card_details = card_details.filter(pros__Neck__neck__in = neck_list).all().distinct()
       if len(pocket_list) > 0:
           card_details = card_details.filter(pros__Pocket__pocket__in = pocket_list).all().distinct()
       if len(sleeve_list) > 0:
           card_details = card_details.filter(pros__Sleeves__sleeves__in = sleeve_list).all().distinct()
       if len(rise_list) > 0:
           card_details = card_details.filter(pros__Rise__in = rise_list).all().distinct()
       if len(stretch_list) > 0:
           card_details = card_details.filter(pros__Stretchable__in = stretch_list).all().distinct()       
       neck = card_details.values_list('pros__Neck__neck',flat=True).exclude(pros__Neck__neck=None).distinct()
       pocket = card_details.values_list('pros__Pocket__pocket',flat=True).exclude(pros__Pocket__pocket=None).distinct()
       sleeve = card_details.values_list('pros__Sleeves__sleeves',flat=True).exclude(pros__Sleeves__sleeves=None).distinct()
       rise = card_details.values_list('pros__Rise',flat=True).exclude(pros__Rise=None).distinct()
       stretch = card_details.values_list('pros__Stretchable',flat=True).exclude(pros__Stretchable=None).distinct()
    if len(discount_list) > 0:
        if len(discount_list) == 1:
           range_value = (int(discount_list[0]),99)
        else:      
           range_value = (min(list(map(int,discount_list))),99)
        card_details = card_details.filter(discount__range = range_value).all().distinct()
    if len(brand_list) > 0:
        card_details = card_details.filter(brand__brand__in = brand_list).all().distinct()
    if len(age_list) > 0:
       card_details = card_details.filter(age__age__in = age_list).all().distinct()
    if len(size_list) > 0:
        card_details = card_details.filter(size__size__in = size_list).all().distinct()
    if len(color_list) > 0:
        card_details = card_details.filter(pros__Color__color__in = color_list).all().distinct()
    if len(material_list) > 0:
        card_details = card_details.filter(pros__Material__material__in = material_list).all().distinct()
    if len(pattern_list) > 0:
        card_details = card_details.filter(pros__Pattern__pattern__in = pattern_list).all().distinct()
    if len(occasion_list) > 0:
        card_details = card_details.filter(pros__Occasion__occasion__in = occasion_list).all().distinct()
    products = card_details.values_list('category__category',flat=True)\
               .exclude(category__category=None).distinct()
    size = card_details.values_list('size__size',flat=True).exclude(size__size=None).distinct().order_by('-size__id')
    brand = card_details.values_list('brand__brand',flat=True).exclude(brand__brand=None).distinct()
    color = card_details.values_list('pros__Color__color',flat=True).exclude(pros__Color__color=None).distinct()
    material =card_details.values_list('pros__Material__material',flat=True).exclude(pros__Material__material=None).distinct()
    pattern = card_details.values_list('pros__Pattern__pattern',flat=True).exclude(pros__Pattern__pattern=None).distinct()
    occasion = card_details.values_list('pros__Occasion__occasion',flat=True).exclude(pros__Occasion__occasion=None).distinct()
    discounts = models.DISCOUNT_CHOICES
    card_details = sortby(card_details,sort_data) 
    all_filts = {'category':products,'age':[],'brand':brand,'discount':discounts,
                   'size':size,'color':color,'material':material,'pattern':pattern,
                   'occasion':occasion,'neck':neck,'pocket':pocket,'sleeve':sleeve,
                   'rise':rise,'stretchable':stretch}
    filt = list(args[1].GET.keys())[len(list(args[1].GET.keys()))-1][:-2]
    filters = {}
    for x,y in all_filts.items():
        if x == filt:
           continue
        value = render_to_string('other_filters.html',{'value':y,'key':x,'gender':args[2]})
        filters[x] = value  
    ajax = render_to_string('cards.html', {'details': card_details}) 
    return {'details':ajax,'filter':filters}

