from django.shortcuts import render,redirect
from .forms import *
from .models import *

def Home(request):
    context = {
        "admin_name":"Dharanish",
        #"role" : "admin",
        "role":"user",
        "age" : 18,
        "numbers" : [1,2,3,4,5]
    }
    return render(request, 'home.html',context)

def about(request):
    return render(request,'about.html')
def contact(request):
    return render(request,'contact.html')
def service(request):
    return render(request,'service.html')
def cart(request):
    context = {
        'product_form':product_form(),
    }
    if request.method == "POST":
        form = product_form(request.POST)
        if form.is_valid():
            form.save()
    return render(request,'cart.html',context)
def order(request):
    products = {
        "products":product.objects.all()
    }
    return render(request,'my_orders.html',products)
def delete_product(request,id):
    selection = product.objects.get(id = id)
    selection.delete()

    return redirect('/Inventory/myorder/')
def update_product(request,id):
    
    selection = product.objects.get(id = id)
    
    context = {
        'product_form' : product_form(instance=selection)
    }
    if request.method == "POST":
        form = product_form(request.POST,instance=selection)
        if form.is_valid():
            form.save()
            return redirect('/Inventory/myorder/')

    return render(request,'cart.html',context)