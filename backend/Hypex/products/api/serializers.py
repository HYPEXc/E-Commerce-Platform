from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer

from ..models import Product, ProductImage, Rating


# Serializer for ProductImage
class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']


# Serializer for Product
class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'slug',
            'name',
            'category',
            'owner',
            'created_at',
            'description',
            'price',
            'main_image',
            'endpoint',
            'path',
            'edit_endpoint',
            'edit_path'
        ]


# Serializer for Rating
class RatingSerializer(ModelSerializer):
    user = StringRelatedField()

    class Meta:
        model = Rating
        fields = [
            'id',
            'user',
            'rating',
            'comment',
            'created_at',
        ]
