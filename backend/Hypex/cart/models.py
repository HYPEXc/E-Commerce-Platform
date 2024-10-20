from django.contrib.auth import get_user_model
from django.db import models

from products.models import Product

User = get_user_model()


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_amount(self):
        return sum(item.total_price for item in self.items.all())

    def __str__(self):
        return f"{self.user.name}'s Cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')  # Updated related_name
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.product.selling_price * self.quantity

    class Meta:
        # Ensure a product can't be added twice for the same user
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity} {self.product.name} in {self.cart.user.name}'s Cart"
