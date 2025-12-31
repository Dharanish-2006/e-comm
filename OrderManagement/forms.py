from django import forms
from Inventory.models import product, ProductImage

class ProductForm(forms.ModelForm):
    class Meta:
        model = product
        fields = ["product_name", "price","description" , "image"]
class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ["image"]
