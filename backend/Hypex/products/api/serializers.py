from rest_framework.fields import CharField
from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer

from ..models import Product, ProductImage, Rating, WishlistItem, Wishlist, Cart, CartItem


# Serializer for ProductImage
class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']


# Serializer for Product
class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'owner', 'created_at', 'description', 'price', 'main_image',
                  'slug']


# Serializer for Rating
class RatingSerializer(ModelSerializer):
    user = StringRelatedField()

    class Meta:
        model = Rating
        fields = ['id', 'user', 'rating', 'comment', 'created_at']


# Serializer for WishlistItem
class WishlistItemSerializer(ModelSerializer):
    product_name = CharField(source='product.name', read_only=True)  # For better readability

    class Meta:
        model = WishlistItem
        fields = ['id', 'product', 'product_name', 'added_at']


# Serializer for Wishlist
class WishlistSerializer(ModelSerializer):
    items = WishlistItemSerializer(many=True, read_only=True)  # Use the new related name

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'title', 'created_at', 'items']


# Serializer for CartItem
class CartItemSerializer(ModelSerializer):
    product_name = CharField(source='product.name', read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'quantity', 'added_at']


# Serializer for Cart
class CartSerializer(ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)  # Use the new related name

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items']
