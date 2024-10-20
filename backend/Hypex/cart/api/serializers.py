from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from cart.models import CartItem, Cart


class CartItemSerializer(ModelSerializer):
    product_name = CharField(source='product.name', read_only=True)

    class Meta:
        model = CartItem
        fields = [
            'id',
            'product',
            'product_name',
            'quantity',
            'total_price',
            'added_at',
        ]
        read_only_fields = ['cart']


# Serializer for Cart
class CartSerializer(ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)  # Use the new related name

    class Meta:
        model = Cart
        fields = [
            'id',
            'user',
            'created_at',
            'items',
        ]
