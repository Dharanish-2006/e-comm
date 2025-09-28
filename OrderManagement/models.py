from django.db import models
from Inventory.models import product,ProductImage
# class Product(models.Model):
#     product_name = models.CharField(max_length=200, null=True)
#     tax = models.FloatField(default=0.00)  
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     is_food_product = models.BooleanField(default=False)
#     image = models.ImageField(upload_to="products/", blank=True, null=True)

#     def __str__(self):
#         return self.product_name
