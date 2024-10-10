from django.db import models

from Hypex.Hypex.utils import unique_file_name
from Hypex.accounts.models import User


class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    main_image = models.ImageField(upload_to=unique_file_name)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    sales_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=unique_file_name)

    def __str__(self):
        return f"Image for {self.product.name}"
