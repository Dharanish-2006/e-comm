from django.urls import path
from .views import *

urlpatterns = [
    path('',login_page),
    path('logout/',LogoutUser),
]
