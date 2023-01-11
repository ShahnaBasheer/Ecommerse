import json,re
from . import models,context_processors,import_fnctns as fncs
from .models import AllFashion,Color, EcomCartItem, Size
from django.template.loader import render_to_string
from django.db.models import Q,Count,Sum,F,Max,Min

def product_page(*args):
    size = args[0].values(pro = F('Sellers__size__sizes')).distinct().all().\
            annotate(count=Count('Products',distinct=True))
    brand = args[0].values(pro = F('brand__brand')).distinct().all().\
            annotate(count = Count('brand',distinct=True))
    color = args[0].values(pro = F('Products__Color__color')).distinct().all().\
            annotate(count=Count('Products',distinct=True))
    material =args[0].values(pro = F('Products__Material')).distinct().all().\
            annotate(count=Count('Products',distinct=True))
    pattern = args[0].values(pro = F('Products__Pattern')).distinct().all().\
            annotate(count=Count('Products',distinct=True))
    occasion = args[0].values(pro = F('Products__Occasion')).distinct().all().\
            annotate(count=Count('Products',distinct=True))
    discounts = args[0].values(pro = F('Sellers__size__discnt_cat')).distinct().all().\
                annotate(count=Count('Products',distinct=True))          
    products = args[0].values(pro = F('category')).distinct().all().\
               annotate(count = Count('category',distinct=True))  
    neck = pocket = sleeve = rise = stretch = []          
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
        card_details = args[0].annotate(price=Max('Sellers__size__price')).order_by('price')
    elif args[1] == ['price_desc']:
        card_details = args[0].annotate(price=Max('Sellers__size__price')).order_by('-price')
    elif args[1] == ['newest']:
        card_details = args[0].order_by('-id')
    elif args[1] == ['disc_desc']:
        card_details = args[0].annotate(discount=Max('Sellers__size__discount')).order_by('-discount')
    elif args[1] == ['delivery']:
        card_details = args[0].filter(Sellers__dlvry_charges = "FREE").all().distinct()
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
       card_details = card_details.filter(category__in = cat_list).all().distinct()
       if len(neck_list) > 0:
          card_details = card_details.filter(Products__Neck__in = neck_list).all().distinct()
       if len(pocket_list) > 0:
           card_details = card_details.filter(Products__Pocket__in = pocket_list).all().distinct()
       if len(sleeve_list) > 0:
           card_details = card_details.filter(Products__Sleeves__in = sleeve_list).all().distinct()
       if len(rise_list) > 0:
           card_details = card_details.filter(Products__Rise__in = rise_list).all().distinct()
       if len(stretch_list) > 0:
           card_details = card_details.filter(Products__Stretchable__in = stretch_list).all().distinct()       
       neck = card_details.values(pro = F('Products__Neck')).exclude(Products__Neck=None).\
              distinct().all().annotate(count = Count('Products',distinct=True))
       pocket = card_details.values(pro = F('Products__Pocket')).exclude(Products__Pocket=None).\
             distinct().all().annotate(count = Count('Products',distinct=True))
       sleeve = card_details.values(pro = F('Products__Sleeves')).exclude(Products__Sleeves=None).\
             distinct().all().annotate(count = Count('Products',distinct=True))
       rise = card_details.values(pro = F('Products__Rise')).exclude(Products__Rise=None).\
             distinct().all().annotate(count = Count('Products',distinct=True))
       stretch = card_details.values(pro = F('Products__Stretchable')).exclude(Products__Stretchable=None).\
             distinct().all().annotate(count = Count('Products',distinct=True))
    if len(discount_list) > 0:
        card_details = card_details.filter(Sellers__size__discnt_cat__in = discount_list).all().distinct()
    if len(brand_list) > 0:       
        card_details = card_details.filter(brand__brand__in = brand_list).all().distinct()
        procs = args[0].filter(brand__brand__in = brand_list).all().distinct()
    if len(age_list) > 0:
        card_details = card_details.filter(age__age__in = age_list).all().distinct()
        procs = args[0].filter(age__age__in = age_list).all().distinct()
    if len(size_list) > 0:
        card_details = card_details.filter(Sellers__size__sizes__in = size_list).all().distinct()
        procs = args[0].filter(Sellers__size__sizes__in = size_list).all().distinct()
    if len(color_list) > 0:
        card_details = card_details.filter(Products__Color__color__in = color_list).all().distinct()
        procs = args[0].filter(Products__Color__color__in = color_list).all().distinct()
    if len(material_list) > 0:
        card_details = card_details.filter(Products__Material__in = material_list).all().distinct()
        procs = args[0].filter(Products__Material__in = material_list).all().distinct()
    if len(pattern_list) > 0:
        card_details = card_details.filter(Products__Pattern__in = pattern_list).all().distinct()
        procs = args[0].filter(Products__Pattern__in = pattern_list).all().distinct()
    if len(occasion_list) > 0:
        card_details = card_details.filter(Products__Occasion__in = occasion_list).all().distinct()
        procs = args[0].filter(Products__Occasion__in = occasion_list).all().distinct()

    size = card_details.values(pro = F('Sellers__size__sizes')).distinct().all().\
            annotate(count=Count('Products',distinct=True))
    brand = card_details.values(pro = F('brand__brand')).distinct().all().\
            annotate(count = Count('brand',distinct=True))
    color = card_details.values(pro = F('Products__Color__color')).distinct().all().\
            annotate(count=Count('Products',distinct=True))
    material = card_details.values(pro = F('Products__Material')).distinct().all().\
            annotate(count=Count('Products',distinct=True))
    pattern = card_details.values(pro = F('Products__Pattern')).distinct().all().\
            annotate(count=Count('Products',distinct=True))
    occasion = card_details.values(pro = F('Products__Occasion')).distinct().all().\
            annotate(count=Count('Products',distinct=True))
    discounts = card_details.values(pro = F('Sellers__size__discnt_cat')).\
            distinct().all().annotate(count=Count('Products',distinct=True)) 
    if checked_lists != 'category':   
        products = procs.values(pro = F('category')).distinct().all().\
            annotate(count=Count('category',distinct=True))
    else:   
        products = card_details.values(pro = F('category')).distinct().all().\
            annotate(count=Count('category',distinct=True))
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


def searchbar(*args):
    allproducts = AllFashion.objects.all() 
    card_details = False
    search = args[1]
    searchType = args[2]  
    color = list(Color.objects.values_list('color',flat=True).all())
    auto_items = context_processors.search_items(args[0])['automate_search'] + color                
    auto_items = [items.lower() for items in auto_items] 
    category = list(allproducts.values_list('category',flat=True).all())
    cat_nospace =[i.lower().replace('-','').replace(' ','') for i in category]
    for_items = ["women","men","girls","boys","kids"]
    split_s = search.split('for')
    split_s = [i.strip() for i in split_s]   
    cat = fncs.checker(cat_nospace,split_s,category)  
    
    if searchType == 'AutomateSearch':    
        if len(split_s) == 2 and any(i in split_s for i in for_items):  
            card_details = allproducts.filter(Q(category__istartswith=cat) & 
                           fncs.gender_checker(split_s[1])).all().distinct()
            
        else:
            card_details = allproducts.filter(Q(category__istartswith=search)|
                         Q(title__iexact=search)|Q(brand__brand__iexact=search)).all().distinct()   
    
    elif searchType == 'ManualSearch':
        if any([search == x for x in auto_items]):
            if len(split_s) == 2 and any(i in split_s for i in for_items):
                card_details = allproducts.filter(Q(category__istartswith=cat) & 
                           fncs.gender_checker(split_s[1])).all().distinct()
                
            else:
                card_details = allproducts.filter(Q(category__istartswith=search)|
                             Q(title__istartswith=search)|Q(brand__brand__iexact=search)|
                             Q(Products__Color__color__icontains=search)).all().distinct()
                  
        elif len(search.split()) > 1 :    
            if re.search(' t shirt|t-shirt|t shirt',search) :
               search = search.replace('t shirt',' tshirt').replace('t-shirt',' tshirt')
               split_s = search.split()
            else:   
               split_s = search.split() 
            split_s = [i.strip() for i in split_s]
            sleeves = list(allproducts.values_list('Products__Sleeves',flat=True).all())
            sleev_nospace = [i.lower().replace('-','').replace(' ','') for i in sleeves]
            sleeve = fncs.checker(sleev_nospace,split_s,sleeves)
            cat =  fncs.checker(cat_nospace,split_s,category)                  
            qs = [Q(Products__Color__color__icontains=i)|Q(brand__brand__iexact=i)for i in split_s] 
            query = qs.pop()
            for q in qs:
                query |= q   
            if len(allproducts.filter(query).all()) == 0:
                query = Q(Products__Sleeves__icontains=sleeve)
                card_details = allproducts.filter(query & Q(category__istartswith=cat) &
                 fncs.gender_checker(split_s)).all().distinct()
            else:
                card_details = allproducts.filter(query & Q(category__istartswith=cat) &
                 fncs.gender_checker(split_s)).all().distinct()
             
    if card_details == False: 
        if re.search(' t shirt|t-shirt|t shirt|tshirt',search) :
            search = search.replace('t shirt','t-shirt').replace('tshirt','t-shirt') 
        card_details = allproducts.filter(Q(category__istartswith=search)|
                  Q (Products__Color__color__icontains=search)|Q(brand__brand__contains=search)|
                  Q (Products__Sleeves__icontains=search[0:3])|Q(title__istartswith=search)|
                  Q (gender__istartswith=search)).all().distinct()
                
    elif len(card_details) == 0:
        card_details = allproducts.filter(Q(title__icontains=search))
    return {'details':card_details}


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