from django.urls import path, include
from rest_framework.routers import DefaultRouter

from cart.api.views import CartItemViewSet

# Router for CartItemViewSet
router = DefaultRouter()
router.register(r'cart-items', CartItemViewSet, basename='cart-item')

urlpatterns = [
    # Include the cart-items URLs from the router
    path('', include(router.urls)),
]
