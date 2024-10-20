from django.contrib.auth import get_user_model
from django.db import models

from products.models import Product

User = get_user_model()


class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wishlist')

    def __str__(self):
        return f"{self.user.name}'s Wishlist"


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')  # Updated related_name
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=6, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], default='medium')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensure a product can't be added twice
        unique_together = ('wishlist', 'product')

    def __str__(self):
        return f"{self.product.name} in {self.wishlist.__str__()}"
