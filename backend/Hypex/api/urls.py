from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # URL endpoint for obtaining access and refresh tokens using JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # URL endpoint for refreshing an existing access token using a refresh token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Include the URLs from the products app under the 'products/' path
    # This will prepend 'products/' to all the URLs defined in the products.api.urls module
    path('products/', include('products.api.urls')),
]
