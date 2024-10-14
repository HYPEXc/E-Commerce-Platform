from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from .permissions import isStaffEditorPermission, IsProductOwnerPermission
from .serializers import ProductsSerializer
from ..models import Product
from ...accounts.models import ProductViewLog, User


class TrendingProductListView(ListAPIView):
    serializer_class = ProductsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication]
    def get_queryset(self):
        # Get the top 10 trending products based on sales_count
        return Product.objects.filter(visible=True).order_by('-sales_count')[:10]


class UserProductListView(ListAPIView):
    serializer_class = ProductsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Get user_id from the URL parameters
        user_id = self.kwargs['user_id']

        # Get the User object or return 404
        user = get_object_or_404(User, pk=user_id)

        return Product.objects.filter(owner=user)


class ProductUpdateView(UpdateAPIView):
    serializer_class = ProductsSerializer
    permission_classes = [IsAuthenticated, isStaffEditorPermission, IsProductOwnerPermission]

    def get_queryset(self):
        # Get user_id from URL or use the authenticated user's ID if not provided
        user_id = self.kwargs.get('user_id', self.request.user.pk)

        # Return only the products owned by the specified user
        return Product.objects.filter(owner_id=user_id)


class ProductAddView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer
    permission_classes = [IsAuthenticated]


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            return Product.objects.get_recommended_products_for_authenticated_user(user)

        else:
            viewed_products_ids = self.request.COOKIES.get('viewed_products', '')
            viewed_products_list = viewed_products_ids.split(',') if viewed_products_ids else []

            return Product.objects.get_recommended_products_for_unauthenticated_user(viewed_products_list)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer
    lookup_field = 'pk'

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        # Get the product being viewed; raises 404 if not found
        product = self.get_object()

        # Log the product view
        if request.user.is_authenticated:
            ProductViewLog.objects.create(product=product, user=request.user)
            return super().retrieve(request, *args, **kwargs)
        else:
            # Handle unauthenticated users
            viewed_products = request.COOKIES.get('viewed_products', '')
            viewed_products_list = viewed_products.split(',') if viewed_products else []

            # Add the current product ID if it's not already in the list
            product_id = str(product.pk)
            if product_id not in viewed_products_list:
                viewed_products_list.append(product_id)

            # Get the response from the super method
            response = super().retrieve(request, *args, **kwargs)

            # Set the cookie that lasts for 90 days
            response.set_cookie('viewed_products', ','.join(viewed_products_list), max_age=60 * 60 * 24 * 90)

            return response
