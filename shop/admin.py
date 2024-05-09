from django import forms
from django.contrib import admin
from django.utils.html import format_html

from .models import Product, ProductImage, ProductSize, ProductColor, Category


# Register your models here.

class ProductColorInline(admin.TabularInline):
    model = ProductColor
    fields = ['color']
    extra = 1


class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    fields = ['size']
    extra = 1


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    fields = ['image']
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductColorInline, ProductSizeInline, ProductImageInline]
    list_display = ["name", "image_tag", "price", "available"]
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']

    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("name",)}

    def image_tag(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 30px; max-width: 30px; border-radius: 100%;" />'.format(obj.image.url))
        else:
            return ""
    image_tag.short_description = 'Primary Image'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'image_tag')  # Add 'image_tag' to list_display

    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("name",)}

    # Define a method to display the image as HTML in the admin
    def image_tag(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 30px; max-width: 30px; border-radius: 100%;" />'.format(
                    obj.image.url))
        else:
            return ""
    # Set the short description for the method (optional)
    image_tag.short_description = 'Image'
