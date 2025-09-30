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
    images = item.images.all()

    if request.method == "POST":
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=item
        )
        if not created:
            cart_item.quantity += 1
        cart_item.save()
        return redirect("cart")

    return render(
        request,
        "product_detail.html",
        {"product": item, "images": images}
    )


def about(request):
    return render(request,'about.html')
def contact(request):
    return render(request,'contact.html')
def service(request):
    return render(request,'service.html')

@login_required
def cart(request):
    if request.method == "POST":
        if "product_id" in request.POST:
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

        elif "checkout" in request.POST:
            Cart.objects.filter(user=request.user).delete()
            return redirect("orders")

    items = Cart.objects.filter(user=request.user)

    total = sum(item.product.price * item.quantity for item in items)

    return render(request, "cart.html", {"items": items, "total": total})

@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Cart, user=request.user, product_id=pk)
    item.delete()
    return redirect("cart")

@login_required
def order(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    orders = orders.prefetch_related('orderitem_set__product')
    return render(request, "my_orders.html", {"orders": orders})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    items = order.orderitem_set.select_related('product')
    return render(request, "order_detail.html", {"order": order, "items": items})


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

@login_required
def checkout(request):
    items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price for item in items)

    return render(request, "checkout.html", {"items": items, "total": total})


@login_required
def place_order(request):
    items = Cart.objects.filter(user=request.user)

    if not items.exists():
        return redirect('cart') 
    order_total = sum(item.total_price for item in items)

    order = Order.objects.create(user=request.user, total=order_total)

    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
    items.delete()

    return render(request, "order_confirmation.html", {
        "order_items": order.orderitem_set.all(),
        "order_total": order_total
    })


@login_required
def increase_quantity(request, item_id):
    item = get_object_or_404(Cart, id=item_id, user=request.user)
    item.quantity += 1
    item.save()
    return redirect("cart")


@login_required
def decrease_quantity(request, item_id):
    item = get_object_or_404(Cart, id=item_id, user=request.user)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect("cart")