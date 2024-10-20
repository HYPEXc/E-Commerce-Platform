from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from ..models import WishlistItem, Wishlist


# Serializer for WishlistItem
class WishlistItemSerializer(ModelSerializer):
    product_name = CharField(source='product.name', read_only=True)

    class Meta:
        model = WishlistItem
        fields = [
            'id',
            'product',
            'product_name',
            'added_at',
        ]


# Serializer for Wishlist
class WishlistSerializer(ModelSerializer):
    items = WishlistItemSerializer(many=True, read_only=True)

    class Meta:
        model = Wishlist
        fields = [
            'id',
            'user',
            'items',
        ]
