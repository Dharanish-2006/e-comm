from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *

def Home(request):
    return render(request, 'home.html')
def about(request):
    return render(request,'about.html')
def contact(request):
    return render(request,'contact.html')
def service(request):
    return render(request,'service.html')

@login_required
def cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        product_obj = get_object_or_404(product, id=product_id)

        # Add to user’s cart
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product_obj
        )
        if not created:
            cart_item.quantity += 1
        cart_item.save()
        return redirect("cart")  # refresh page

    # Show only the logged-in user’s cart
    items = Cart.objects.filter(user=request.user)
    return render(request, "cart.html", {"items": items})
def order(request):
    products = {
        "products":product.objects.all()
    }
    return render(request,'my_orders.html',products)
def delete_product(request,id):
    selection = product.objects.get(id = id)
    selection.delete()

    return redirect('/home/myorder/')
def update_product(request,id):
    
    selection = product.objects.get(id = id)
    
    context = {
        'product_form' : product_form(instance=selection)
    }
    if request.method == "POST":
        form = product_form(request.POST,instance=selection)
        if form.is_valid():
            form.save()
            return redirect('/home/myorder/')

    return render(request,'cart.html',context)