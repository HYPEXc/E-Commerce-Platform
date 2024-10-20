from django.urls import path, include

urlpatterns = [
    # Include the URLs from the products app under the 'products/' path
    # This will prepend 'products/' to all the URLs defined in the products.api.urls module
    path('products/', include('products.api.urls')),
]
