from django.urls import path
from .views import *

urlpatterns = [
    path('home/',Home),
    path('about/',about),
    path('service/',service),
    path('contact/',contact),
    path('cart/',cart),
    path('myorder/',order),
    path('cancelorder/<int:id>/',delete_product,name='delete_product'),
    path('updateorder/<int:id>/',update_product,name='update_product'),
]