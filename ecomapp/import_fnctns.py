import json
from . import models
from .models import EcomCartItem
from django.template.loader import render_to_string
from django.db.models import Q,Count,Sum,F

def product_page(*args):
    size = args[0].values(pro = F('size__size')).exclude(size__size=None).order_by('size__id').annotate(count = Count('size'))
    brand = args[0].values(pro = F('brand__brand')).annotate(count = Count('brand'))
    color = args[0].values(pro = F('pros__Color__color')).annotate(count=Count('pros__Color'))
    material =args[0].values(pro = F('pros__Material__material')).annotate(count=Count('pros__Material'))
    pattern = args[0].values(pro = F('pros__Pattern__pattern')).annotate(count=Count('pros__Pattern'))
    occasion = args[0].values(pro = F('pros__Occasion__occasion')).annotate(count=Count('pros__Occasion'))
    discounts = models.DISCOUNT_CHOICES
    neck = pocket = sleeve = rise = stretch = [] 
    products = args[0].values(pro = F('category__category')).annotate(count = Count('category'))           
    context = {
      'allproducts':{'category':products,'age':None,'brand':brand,'discount':discounts,
                   'size':size,'color':color,'material':material,'pattern':pattern,
                   'occasion':occasion,'neck':neck,'pocket':pocket,'sleeve':sleeve,
                   'rise':rise,'stretchable':stretch},
      'details':args[0],
      'gender':args[1],
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
    cart_obj = EcomCartItem.objects.filter(cart=cart)
    if len(cart_obj) == 0:
      cart.delete()
    else:
      cart.total_qty = cart_obj.aggregate(quantity=Sum('quantity'))['quantity']  
      cart.total_amnt = cart_obj.aggregate(total_price=Sum('total_price'))['total_price']
      cart.total_dscnt = cart_obj.aggregate(total_mrp=Sum('total_mrp'))['total_mrp'] - cart.total_amnt
      cart.dlvry_chrg = cart_obj.aggregate(delivery=Sum('delivery'))['delivery']
      cart.save()

def product_filters(*args):
    card_details = procs = args[0]
    gender_list = args[1].GET.getlist('gender[]')
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
    checked_lists = args[1].GET['_checked']
    neck = pocket = sleeve = rise = stretch = []
    if len(gender_list) > 0:
       card_details = card_details.filter(gender__in = gender_list).all().distinct()
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
       neck = card_details.values(pro = F('pros__Neck__neck')).exclude(pros__Neck__neck=None).annotate(count = Count('pros__Neck'))
       pocket = card_details.values(pro = F('pros__Pocket__pocket')).exclude(pros__Pocket__pocket=None).annotate(count = Count('pros__Pocket'))
       sleeve = card_details.values(pro = F('pros__Sleeves__sleeves')).exclude(pros__Sleeves__sleeves=None).annotate(count = Count('pros__Sleeves'))
       rise = card_details.values(pro = F('pros__Rise')).exclude(pros__Rise=None).annotate(count = Count('pros__Rise'))
       stretch = card_details.values(pro = F('pros__Stretchable')).exclude(pros__Stretchable=None).annotate(count = Count('pros__Stretchable'))
    if len(discount_list) > 0:
        if len(discount_list) == 1:
           range_value = (int(discount_list[0]),99)
        else:      
           range_value = (min(list(map(int,discount_list))),99)
        card_details = card_details.filter(discount__range = range_value).all().distinct()
    if len(brand_list) > 0:       
        card_details = card_details.filter(brand__brand__in = brand_list).all().distinct()
        procs = args[0].filter(brand__brand__in = brand_list).all().distinct()
    if len(age_list) > 0:
        card_details = card_details.filter(age__age__in = age_list).all().distinct()
        procs = args[0].filter(age__age__in = age_list).all().distinct()
    if len(size_list) > 0:
        card_details = card_details.filter(size__size__in = size_list).all().distinct()
        procs = args[0].filter(size__size__in = size_list).all().distinct()
    if len(color_list) > 0:
        card_details = card_details.filter(pros__Color__color__in = color_list).all().distinct()
        procs = args[0].filter(pros__Color__color__in = color_list).all().distinct()
    if len(material_list) > 0:
        card_details = card_details.filter(pros__Material__material__in = material_list).all().distinct()
        procs = args[0].filter(pros__Material__material__in = material_list).all().distinct()
    if len(pattern_list) > 0:
        card_details = card_details.filter(pros__Pattern__pattern__in = pattern_list).all().distinct()
        procs = args[0].filter(pros__Pattern__pattern__in = pattern_list).all().distinct()
    if len(occasion_list) > 0:
        card_details = card_details.filter(pros__Occasion__occasion__in = occasion_list).all().distinct()
        procs = args[0].filter(pros__Occasion__occasion__in = occasion_list).all().distinct()

    size = card_details.values(pro = F('size__size')).exclude(size__size=None).order_by('size__id').annotate(count = Count('size'))
    brand = card_details.values(pro = F('brand__brand')).annotate(count = Count('brand'))
    color = card_details.values(pro = F('pros__Color__color')).annotate(count=Count('pros__Color'))
    material =card_details.values(pro = F('pros__Material__material')).annotate(count=Count('pros__Material'))
    pattern = card_details.values(pro = F('pros__Pattern__pattern')).annotate(count=Count('pros__Pattern'))
    occasion = card_details.values(pro = F('pros__Occasion__occasion')).annotate(count=Count('pros__Occasion'))
    discounts = models.DISCOUNT_CHOICES
    if checked_lists != 'category':   
        products = procs.values(pro = F('category__category')).annotate(count=Count('category'))
    else:   
        products = card_details.values(pro = F('category__category')).annotate(count=Count('category'))
    card_details = sortby(card_details,sort_data)
    
    all_filts = {'category':products,'age':[],'brand':brand,'discount':discounts,
                   'size':size,'color':color,'material':material,'pattern':pattern,
                   'occasion':occasion,'neck':neck,'pocket':pocket,'sleeve':sleeve,
                   'rise':rise,'stretchable':stretch}
    #check_lists =([i[:-2] for i in filt])
    filters = {}
    for x,y in all_filts.items():
        if x == checked_lists:
           continue
        value = render_to_string('other_filters.html',{'value':y,'key':x,'gender':args[2]})
        filters[x] = value  
    ajax = render_to_string('cards.html', {'details': card_details}) 
    json_str = json.dumps(card_details.count())
    return {'details':ajax,'filter':filters,'count':json_str}


def checker(set_nospace,splits,sets):
        setindex = ''
        for x in set_nospace:
          for s in splits:
              s = s.replace(' ','').replace('-','')
              if x.startswith(s):
                  setindex = sets[set_nospace.index(x)]                
        return setindex


def gender_checker(genders):
    if type(genders) == type([]):
        if any(i for i in ['women','men','girls','boys','kids'] if i in genders):
            for gender in genders:
               if gender == 'kids':
                  lookup = Q(gender__in = ['girls','boys']) 
               else:
                  lookup = Q(gender = gender)               
        else:         
            lookup = Q(gender__in = ['women','men','girls','boys'])                    
    else:
        if genders == 'kids':
           lookup = Q(gender__in = ['girls','boys'])
        else:
           lookup = Q(gender__iexact = genders)
    return lookup                     