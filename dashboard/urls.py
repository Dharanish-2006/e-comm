from django.urls import path
from .views import *

urlpatterns = [
    path('',dashboard_view),
    path('update-layout/', update_layout, name='update_layout'),
]