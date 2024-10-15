from django.db import models
from django.db.models import Q

from accounts.models import User


# from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Keyword(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class ProductManager(models.Manager):
    def get_recommended_products_for_authenticated_user(self, user, request):
        # Get viewed products from ProductViewLog
        viewed_logs = ProductViewLog.objects.filter(user=user).select_related('product')
        viewed_products = [log.product for log in viewed_logs]

        # Retrieve viewed products from cookies
        viewed_products_cookies = request.COOKIES.get('viewed_products', '')
        viewed_products_list = viewed_products_cookies.split(',') if viewed_products_cookies else []

        # Get products based on cookie IDs that are visible
        viewed_products_from_cookies = Product.objects.filter(
            id__in=[int(pid) for pid in viewed_products_list if pid.isdigit()],
            visible=True,  # Check if product is visible
        )

        # Combine viewed products from logs and cookies
        combined_viewed_products = viewed_products + list(viewed_products_from_cookies)

        # Collect categories and keywords from viewed products
        categories = set()
        keywords = set()
        for product in combined_viewed_products:
            categories.add(product.category)
            keywords.update(product.keywords.all())

        # Recommendations based on categories and keywords, ensuring products are visible
        recommended_products = self.filter(
            Q(category__in=categories) | Q(keywords__in=keywords),
            visible=True  # Check if product is visible
        ).exclude(pk__in=[product.pk for product in combined_viewed_products]).distinct()

        # Get related products based on categories and keywords, ensuring they are visible
        related_products = self.filter(
            Q(category__in=categories) | Q(keywords__in=keywords),
            visible=True
        ).exclude(pk__in=[product.pk for product in combined_viewed_products]).distinct()

        # Combine all products ensuring distinct products
        all_recommended_products = list(recommended_products) + list(related_products)

        # Limit the total recommendations to 200 products
        all_recommended_products = list(set(all_recommended_products))  # Remove duplicates
        if len(all_recommended_products) > 200:
            all_recommended_products = all_recommended_products[:200]

        # If less than 200 products are found, add random visible products to fill up to 200
        if len(all_recommended_products) < 200:
            random_products = self.exclude(pk__in=[product.pk for product in all_recommended_products]) \
                                  .filter(visible=True).order_by('?')[
                              :200 - len(all_recommended_products)]  # Ensure random products are visible

            # Combine random products to reach the limit of 200
            all_recommended_products += list(random_products)

        return all_recommended_products[:200]  # Ensure the final list does not exceed 200 products

    def get_recommended_products_for_unauthenticated_user(self, viewed_product_ids):
        # Recommendations based on product IDs in cookies that are visible
        recommended_products = self.filter(
            pk__in=viewed_product_ids,
            visible=True  # Check if product is visible
        ).distinct()

        # If no products found, return random visible products
        if not recommended_products.exists():
            recommended_products = self.filter(visible=True).order_by('?')[:10]  # Ensure random products are visible

        # Ensure total recommendations do not exceed 200 products
        if recommended_products.count() > 200:
            recommended_products = recommended_products[:200]

        return recommended_products


class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    main_image = models.ImageField(upload_to='products/')
    owner = models.ForeignKey('accounts.User', on_delete=models.CASCADE)  # Use string here
    sales_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    keywords = models.ManyToManyField(Keyword, related_name='products')
    visible = models.BooleanField(default=True)

    objects = ProductManager()

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    from Hypex.utils import unique_file_name
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)

    # Using a unique upload path function
    image = models.ImageField(upload_to=unique_file_name)

    def __str__(self):
        return f"Image for {self.product.name}"


class ProductViewLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    view_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} viewed {self.product} on {self.view_date}"