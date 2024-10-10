from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.viewsets import ModelViewSet

from ..models import Product
from .serializers import LimitedProductSerializer, ItemsSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.filter().order_by('-id')
    serializer_class = ItemsSerializer


class TrendingProductsView(ListAPIView):
    queryset = Product.objects.order_by('-sales_count')[:10]
    serializer_class = LimitedProductSerializer
