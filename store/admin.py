from django.contrib import admin
from django.utils.html import mark_safe
from .models import Product, Category, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="80" height="80" style="object-fit: cover; border-radius: 6px;"/>')
        return "No Image"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "category", "stock", "thumbnail")
    list_filter = ("category",)
    search_fields = ("name", "description")
    inlines = [ProductImageInline]

    def thumbnail(self, obj):
        """Show the first image as a small thumbnail in the list view."""
        first_image = obj.images.first()
        if first_image and first_image.image:
            return mark_safe(f'<img src="{first_image.image.url}" width="50" height="50" style="object-fit: cover; border-radius: 4px;"/>')
        return "—"
    thumbnail.short_description = "Preview"


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "image")
