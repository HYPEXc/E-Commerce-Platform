from io import BytesIO

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase
from django.urls import reverse
from uuid import uuid4
from products.models import Product, Category, Keyword

User = get_user_model()


class ProductAPITests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username=f'testuser_{uuid4()}', password='testpass')

        # Create a test category
        self.category = Category.objects.create(name=f'Test Category {uuid4()}')

        # Create a test keyword
        self.keyword = Keyword.objects.create(name=f'Test Keyword {uuid4()}')

        # Create a test product first (without assigning keywords)
        self.product = Product.objects.create(
            name=f'Test Product {uuid4()}',
            description='Test description',
            price=99.99,
            owner=self.user,
            visible=True,
            category=self.category,
        )

        # Assign the keyword using set() after the product has been created
        self.product.tags.set([self.keyword])

        # Obtain a token for the test user
        response = self.client.post(reverse('token_obtain_pair'), {
            'username': self.user.username,
            'password': 'testpass'
        })
        self.token = response.data['access']

    def test_product_list_authenticated(self):
        # Test that authenticated users can access the product list using token
        response = self.client.get(reverse('product-list'),
                                   HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')

    def test_product_detail_view(self):
        # Test the detail view of a specific product using token
        response = self.client.get(reverse('product-detail', kwargs={'pk': self.product.pk}),
                                   HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test description')

    def test_product_add_view(self):
        # Create test user, category, and keyword if not already present
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name='Test Category')
        self.keyword = Keyword.objects.create(name='Test Keyword')

        # Create a dummy image to upload
        image = Image.new('RGB', (100, 100))  # Create a simple 100x100 RGB image
        image_file = BytesIO()
        image.save(image_file, format='PNG')
        image_file.seek(0)  # Reset the file pointer to the beginning
        uploaded_image = InMemoryUploadedFile(image_file, None, 'test_image.png', 'image/png',
                                              image_file.getbuffer().nbytes, None)

        # Add the token manually in the headers
        response = self.client.post(
            reverse('product-add'),
            {
                'name': 'New Product',
                'description': 'New Description',
                'price': 50.00,
                'owner': self.user.pk,
                'category': self.category.pk,
                'keywords': [self.keyword.pk],
                'main_image': uploaded_image,  # Include the uploaded image here
            },
            HTTP_AUTHORIZATION='Bearer ' + self.token
        )

        self.assertEqual(response.status_code, 201)  # Expected status code for created
        self.assertTrue(Product.objects.filter(name='New Product').exists())
