from django.db import models

class product(models.Model):
    product_name = models.CharField(max_length=200,null=True)
    tax = models.FloatField(default=0.00)  
    price = models.IntegerField(default=0)
    is_food_product = models.BooleanField(default=False)

    def __str__(self):
        return self.product_name