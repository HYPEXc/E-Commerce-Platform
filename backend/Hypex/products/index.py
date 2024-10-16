from algoliasearch_django import AlgoliaIndex as Index
from algoliasearch_django.decorators import register
from .models import Product


@register(Product)
class ProductIndex(Index):
    should_index = 'is_public'
    fields = [
        'name',
        'description',
        'owner',
        'category',
        'main_image',
        'price',
        'rating'
    ]
    settings = {
        'searchableAttributes': ['name', 'category', 'owner', 'description'],
        'attributesForFaceting': ['owner', 'category'],
    }
    tags = 'get_tags_list'
