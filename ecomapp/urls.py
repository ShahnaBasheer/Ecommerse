from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name="homepage"),
    path('women/',views.womentab,name="womenpage"),
    path('men/',views.mentab,name="menpage"),
    path('kids/',views.kidstab,name="kidspage"),
    path('women/category',views.womenproducts,name="w_products"),
    path('men/category',views.menproducts,name="m_products"),
]
