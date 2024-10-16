from django.contrib import admin
from .models import Product, ProductImage, Category, Keyword


# Custom admin class to manage how the Product model appears in the admin interface
class ProductAdmin(admin.ModelAdmin):
    # Fields to display in the list view of the admin panel
    list_display = ('name', 'price', 'category', 'owner', 'public', 'created_at', 'updated_at')

    # Fields that are clickable links, allowing you to access the detailed view
    list_display_links = ('name',)

    # Fields to add filters in the admin list view (for quick filtering)
    list_filter = ('public', 'category', 'owner', 'created_at')

    # Fields to search within (enabling a search bar in the admin)
    search_fields = ('name', 'description', 'category__name', 'owner__username')

    # Fields that are read-only in the admin interface
    readonly_fields = ('created_at', 'updated_at', 'sales_count')

    # Fields to organize the form view in sections
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'price', 'main_image', 'category', 'tags', 'owner', 'public')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
        ('Sales Info', {
            'fields': ('sales_count',)
        }),
    )

    # Inline model to manage related images directly in the Product admin form
    class ProductImageInline(admin.TabularInline):
        model = ProductImage
        extra = 1  # Number of empty image forms provided by default

    # Adding the inline model to the Product admin form
    inlines = [ProductImageInline]

    # Enable the ability to save and continue editing
    save_on_top = True

    # Prepopulating the slug field (if there's any slug field) based on the product name
    # prepopulated_fields = {"slug": ("name",)}  # Uncomment if you have a slug field


# Simple admin registration for Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display the name of the category
    search_fields = ('name',)  # Add a search bar to search categories by name


# Simple admin registration for Keyword
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display the name of the keyword
    search_fields = ('name',)  # Add a search bar to search keywords by name


# Registering the Product model with the custom ProductAdmin
admin.site.register(Product, ProductAdmin)

# Registering the Category and Keyword models with simple ModelAdmin
admin.site.register(Category, CategoryAdmin)
admin.site.register(Keyword, KeywordAdmin)
