from django.urls import path
from .views import *

urlpatterns = [
    path('', Home, name="home"),
    path('about/',about),
    path('service/',service),
    path('contact/',contact),
    path('cart/',cart,name="cart"),
    path("cart/remove/<int:pk>/", remove_from_cart, name="remove_from_cart"),
    path('myorder/',order,name="orders"),
    path('cancelorder/<int:id>/',delete_product,name='delete_product'),
    path('updateorder/<int:id>/',update_product,name='update_product'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
]