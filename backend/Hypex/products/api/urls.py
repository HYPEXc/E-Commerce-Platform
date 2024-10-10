from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TrendingProductsView, ProductViewSet

# Create a router and register your ProductViewSet if needed for CRUD operations
router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('trending/', TrendingProductsView.as_view(), name='trending-products'),
    path('', include(router.urls)),
]

# Register this urls in the main file
