from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Q, Avg
from django.utils.text import slugify

from Hypex.utils import unique_file_name

User = get_user_model()


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

        # Retrieve viewed products from cookies (now using slugs)
        viewed_products_cookies = request.COOKIES.get('viewed_products', '')
        viewed_products_slugs = viewed_products_cookies.split(',') if viewed_products_cookies else []

        # Get products based on cookie slugs that are visible
        viewed_products_from_cookies = Product.objects.filter(
            slug__in=[slug for slug in viewed_products_slugs],
            visible=True,  # Check if product is visible
        )

        # Combine viewed products from logs and cookies
        combined_viewed_products = viewed_products + list(viewed_products_from_cookies)

        # Collect categories and keywords from viewed products
        categories = set()
        keywords = set()
        for product in combined_viewed_products:
            categories.add(product.category)
            keywords.update(product.tags.all())

        # Recommendations based on categories and keywords, ensuring products are visible
        recommended_products = self.filter(
            Q(category__in=categories) | Q(keywords__in=keywords),
            visible=True  # Check if product is visible
        ).exclude(slug__in=[product.slug for product in combined_viewed_products]).distinct()

        # Get related products based on categories and keywords, ensuring they are visible
        related_products = self.filter(
            Q(category__in=categories) | Q(keywords__in=keywords),
            visible=True
        ).exclude(slug__in=[product.slug for product in combined_viewed_products]).distinct()

        # Combine all products ensuring distinct products
        all_recommended_products = list(recommended_products) + list(related_products)

        # Limit the total recommendations to 200 products
        all_recommended_products = list(set(all_recommended_products))  # Remove duplicates
        if len(all_recommended_products) > 200:
            all_recommended_products = all_recommended_products[:200]

        # If less than 200 products are found, add random visible products to fill up to 200
        if len(all_recommended_products) < 200:
            random_products = self.exclude(slug__in=[product.slug for product in all_recommended_products]) \
                                  .filter(visible=True).order_by('?')[
                              :200 - len(all_recommended_products)]  # Ensure random products are visible

            # Combine random products to reach the limit of 200
            all_recommended_products += list(random_products)

        return all_recommended_products[:200]  # Ensure the final list does not exceed 200 products

    def get_recommended_products_for_unauthenticated_user(self, viewed_product_slugs):
        # Recommendations based on product slugs in cookies that are visible
        recommended_products = self.filter(
            slug__in=viewed_product_slugs,
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
    main_image = models.ImageField(upload_to=unique_file_name)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    sales_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    tags = models.ManyToManyField(Keyword, related_name='products')
    public = models.BooleanField(default=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)

    objects = ProductManager()

    @property
    def visible(self):
        return self.public

    def is_public(self):
        return self.public

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Automatically create slug from name
        super().save(*args, **kwargs)

    def get_tags_list(self):
        """Return a list of tag names associated with the product."""
        return [tag.name for tag in self.tags.all()]

    def rating(self):
        """Returns the average rating for this product."""
        ratings = self.ratings.all()
        if ratings.exists():
            return ratings.aggregate(Avg('rating'))['rating__avg']
        return 0.0

    def __str__(self):
        return self.name


class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(
        default=0,
        validators=[MinValueValidator(1), MaxValueValidator(5)]  # Rating between 1 and 5
    )
    comment = models.TextField(blank=True)  # Optional comment
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Ensure each user can only rate a product once
        unique_together = ('product', 'user')


class ProductImage(models.Model):
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


class SearchLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    query = models.CharField(max_length=255)
    search_date = models.DateTimeField(auto_now_add=True)
    keywords = models.ManyToManyField(Keyword, related_name='search_logs', blank=True)

    def __str__(self):
        return f"{self.user} searched for '{self.query}' on {self.search_date}"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # A title field for the wishlist if you want users to name them
    title = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name}'s Wishlist"

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')  # Updated related_name
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensure a product can't be added twice
        unique_together = ('wishlist', 'product')

    def __str__(self):
        return f"{self.product.name} in {self.wishlist.__str__()}"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name}'s Cart"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')  # Updated related_name
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensure a product can't be added twice for the same user
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity} {self.product.name} in {self.cart.user.name}'s Cart"
