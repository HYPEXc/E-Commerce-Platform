from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from .permissions import IsStaffEditorPermission, IsProductOwnerPermission
from .serializers import ProductSerializer
from ..models import Product, ProductViewLog

User = get_user_model()


class TrendingProductListView(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        # Get the top 10 trending products based on sales_count
        return Product.objects.filter(visible=True).order_by('-sales_count')[:10]


class UserProductListView(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Get user_id from the URL parameters
        user_id = self.kwargs['user_id']

        # Get the User object or return 404
        user = get_object_or_404(User, pk=user_id)

        return Product.objects.filter(owner=user)


class ProductUpdateView(UpdateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsStaffEditorPermission, IsProductOwnerPermission]

    def get_queryset(self):
        # Get user_id from URL or use the authenticated user's ID if not provided
        user_id = self.kwargs.get('user_id', self.request.user.pk)

        # Get the product by slug from the URL
        slug = self.kwargs.get('slug')

        # Return only the product with the matching slug and owned by the user
        return Product.objects.filter(owner_id=user_id, slug=slug)


class ProductAddView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            # Fetch recommended products for authenticated users (no change needed)
            return Product.objects.get_recommended_products_for_authenticated_user(user=user, request=self.request)

        else:
            # For unauthenticated users, fetch based on viewed product slugs
            viewed_products_slugs = self.request.COOKIES.get('viewed_products', '')
            viewed_products_list = viewed_products_slugs.split(',') if viewed_products_slugs else []

            # Recommend products based on the viewed products (by slug)
            return Product.objects.get_recommended_products_for_unauthenticated_user(viewed_products_list)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        # Get the product being viewed using the slug; raises 404 if not found
        product = self.get_object()

        # Log the product view for authenticated users
        if request.user.is_authenticated:
            ProductViewLog.objects.create(product=product, user=request.user)
            return super().retrieve(request, *args, **kwargs)
        else:
            # Handle unauthenticated users by logging views in cookies
            viewed_products = request.COOKIES.get('viewed_products', '')
            viewed_products_list = viewed_products.split(',') if viewed_products else []

            # Add the current product slug if it's not already in the list
            product_slug = product.slug
            if product_slug not in viewed_products_list:
                viewed_products_list.append(product_slug)

            # Get the response from the super method
            response = super().retrieve(request, *args, **kwargs)

            # Set the cookie that lasts for 90 days
            response.set_cookie('viewed_products', ','.join(viewed_products_list), max_age=60 * 60 * 24 * 90)

            return response
