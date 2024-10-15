from rest_framework.serializers import ModelSerializer
from ..models import Product, ProductImage


class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']

class ProductsSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
