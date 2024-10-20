from django.urls import path

from .views import (
    TrendingProductListView,
    UserProductListView,
    ProductUpdateView,
    ProductAddView,
    ProductListView,
    ProductDetailView,
)

app_name = 'products'

urlpatterns = [
    # List recommended + random products, can return up to 200 products.
    path('', ProductListView.as_view(), name='product-list'),

    # Retrieve a single product by slug
    path('<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),

    # Add a new product (authenticated users only)
    path('add/', ProductAddView.as_view(), name='product-add'),

    # Update a specific user's product by product slug
    path('update/<slug:slug>/', ProductUpdateView.as_view(), name='product-update'),

    # List trending products (based on sales count)
    path('trending/', TrendingProductListView.as_view(), name='trending-products'),

    # List products for a specific user by their user ID
    path('users/<int:user_id>/', UserProductListView.as_view(), name='user-products'),
]
