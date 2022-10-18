from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name="homepage"),
    path('women/',views.womentab,name="womenpage"),
    path('men/',views.mentab,name="menpage"),
    path('kids/',views.kidstab,name="kidspage"),
    path('women/filter_data',views.filter_women,name="women_filter"),
    path('men/filter_data',views.filter_men,name="men_filter"),
    path('girls/filter_data',views.filter_girls,name="girls_filter"),
    path('boys/filter_data',views.filter_boys,name="boys_filter"),
    path('kids/filter_data',views.filter_kids,name="kids_filter"),
]