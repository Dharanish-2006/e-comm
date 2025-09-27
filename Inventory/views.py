from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from dashboard.models import *

@login_required
def Home(request):
    dashboard, _ = Dashboard.objects.get_or_create(user=request.user)
    widgets = Widget.objects.all()
    query = request.GET.get("q")
    if query:
        products = product.objects.filter(product_name__icontains=query)
    else:
        products = product.objects.all()[:10]
    return render(request, "home.html", {
        "dashboard": dashboard,
        "widgets": widgets,
        "products": products
    })


@login_required
def product_detail(request, pk):
    item = get_object_or_404(product, pk=pk)
    if request.method == "POST":
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=item
        )
        if not created:
            cart_item.quantity += 1
        cart_item.save()
        return redirect("cart")
    return render(request, "product_detail.html", {"product": item})

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
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product_obj
        )
        if not created:
            cart_item.quantity += 1
        cart_item.save()
        return redirect("cart")
    products = product.objects.all()[:10]
    items = Cart.objects.filter(user=request.user)

    for item in items:
        item.line_total = item.product.price * item.quantity

    total = sum(item.line_total for item in items)

    return render(request, "cart.html", {
        "products": products,
        "items": items,
        "total": total
    })

@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Cart, user=request.user, product_id=pk)
    item.delete()
    return redirect("cart")

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