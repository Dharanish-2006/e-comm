from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import product as Product,ProductImage
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
