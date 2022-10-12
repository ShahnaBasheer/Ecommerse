from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name="homepage"),
    path('women/',views.womentab,name="womenpage"),
    path('men/',views.mentab,name="menpage"),
    path('kids/',views.kidstab,name="kidspage"),
    path('women/categories',views.filter_women,name="women_category"),
    path('men/categories',views.filter_men,name="men_category"),
]