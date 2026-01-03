import razorpay
from OrderManagement.utils.email import send_order_confirmation_email
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from Inventory.models import Cart
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from Inventory.models import product as Product, ProductImage
from .models import Order, OrderItem, Payment
from .forms import ProductForm,ProductImageForm
from django.forms import modelformset_factory

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, "OrderManagement/product_list.html", {"products": products})

ProductImageFormSet = modelformset_factory(ProductImage, form=ProductImageForm, extra=3)

@login_required
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        formset = ProductImageFormSet(request.POST, request.FILES, queryset=ProductImage.objects.none())

        if form.is_valid() and formset.is_valid():
            product = form.save()

            for subform in formset:
                if subform.cleaned_data.get("image"):
                    ProductImage.objects.create(product=product, image=subform.cleaned_data["image"])
            return redirect("product_list")
    else:
        form = ProductForm()
        formset = ProductImageFormSet(queryset=ProductImage.objects.none())
    return render(request, "OrderManagement/product_form.html", {"form": form, "formset": formset})


from django.forms import modelformset_factory

ProductImageFormSet = modelformset_factory(ProductImage, form=ProductImageForm, extra=3, can_delete=True)

@login_required
def product_edit(request, pk):
    item = get_object_or_404(Product, pk=pk)
    
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=item)
        formset = ProductImageFormSet(request.POST, request.FILES, queryset=ProductImage.objects.filter(product=item))
        
        if form.is_valid() and formset.is_valid():
            form.save()
            
            for subform in formset:
                if subform.cleaned_data.get("id") and subform.cleaned_data.get("DELETE"):
                    subform.cleaned_data["id"].delete()
                elif subform.cleaned_data.get("image"):
                    image_instance = subform.save(commit=False)
                    image_instance.product = item
                    image_instance.save()
            
            return redirect("orders")
    else:
        form = ProductForm(instance=item)
        formset = ProductImageFormSet(queryset=ProductImage.objects.filter(product=item))
    
    return render(request, "OrderManagement/product_edit.html", {
        "form": form,
        "formset": formset
    })


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect("product_list")
    return render(request, "OrderManagement/product_delete.html", {"product": product})

@login_required
def create_cod_order(request):
    items = Cart.objects.filter(user=request.user)
    if not items.exists():
        return JsonResponse({"status": "error"})

    total = sum(item.total_price for item in items)

    order = Order.objects.create(
        user=request.user,
        full_name=request.session.get("full_name", ""),
        address=request.session.get("address", ""),
        city=request.session.get("city", ""),
        postal_code=request.session.get("postal_code", ""),
        country=request.session.get("country", ""),
        total_amount=total,
        payment_method="COD",
        payment_status="SUCCESS"
    )
    order.status = "CONFIRMED"
    order.save()
    send_order_confirmation_email(order)
    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
        )

    items.delete()

    return JsonResponse({"status": "success"})


@login_required
def create_razorpay_order(request):
    items = Cart.objects.filter(user=request.user)
    if not items.exists():
        return JsonResponse({"error": "Cart empty"}, status=400)

    total = sum(item.total_price for item in items)
    amount = int(total * 100)

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    razorpay_order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    request.session["razorpay_order_id"] = razorpay_order["id"]
    request.session["order_total"] = total

    return JsonResponse({
        "order_id": razorpay_order["id"],
        "amount": amount,
        "key": settings.RAZORPAY_KEY_ID
    })

@csrf_exempt
def verify_payment(request):
    if request.method == "POST":
        data = request.POST

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        try:
            client.utility.verify_payment_signature({
                "razorpay_order_id": data["razorpay_order_id"],
                "razorpay_payment_id": data["razorpay_payment_id"],
                "razorpay_signature": data["razorpay_signature"],
            })

            items = Cart.objects.filter(user=request.user)
            total = request.session.get("order_total")

            order = Order.objects.create(
                user=request.user,
                total_amount=total,
                payment_method="ONLINE",
                payment_status="SUCCESS",
                status="PAID",
                razorpay_order_id=data["razorpay_order_id"]
            )

            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            items.delete()
            send_order_confirmation_email(order)
            return JsonResponse({"status": "success"})

        except Exception as e:
            return JsonResponse({"status": "failed", "error": str(e)})
 
@login_required
def order_success(request):
    return render(request, "order_confirmation.html")