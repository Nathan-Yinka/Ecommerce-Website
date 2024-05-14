from django.db import models
from django.db.models import Q
from taggit.managers import TaggableManager

from myshop.utils import generate_unique_slug


def product_image_upload_path(instance, filename):
    # Construct the upload path dynamically based on the product's slug
    return f"product/images/{instance.product.slug}/{filename}"


def product_primary_image_upload_path(instance, filename):
    # Construct the upload path dynamically based on the product's slug
    return f"product/images/{instance.slug}/{filename}"


def category_image_upload_path(instance, filename):
    # Construct the upload path dynamically based on the product's slug
    return f"category/{instance.slug}-{filename}"


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to=category_image_upload_path, null=True, blank=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = 'categories'

    def save(self, *args, **kwargs):
        self.slug = generate_unique_slug(self, 'slug', 'name')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def search(self, query=None, min_price=None, max_price=None, tags=None, colors=None):
        queryset = self

        lookups = Q()
        if query:
            lookups |= Q(name__icontains=query) | Q(description__icontains=query) | Q(tags__name__icontains=query) | Q(category__name__icontains=query)

        if min_price is not None:
            lookups &= Q(price__gte=min_price)
        if max_price is not None:
            lookups &= Q(price__lte=max_price)

        if tags:
            lookups &= Q(tags__name__in=tags)

        if colors:
            lookups &= Q(colors__color__in=colors)

        queryset = queryset.filter(lookups)
        return queryset.distinct()

    def available(self):
        return self.filter(available=True)


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def search(self, query=None, min_price=None, max_price=None, tags=None, colors=None):
        return self.get_queryset().search(query=query, min_price=min_price, max_price=max_price, tags=tags,
                                          colors=colors)

    def available(self):
        return self.get_queryset().available()


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=product_primary_image_upload_path, help_text="This the primary image for the "
                                                                                     "product")
    description = models.TextField(help_text="Description for the product")
    short_description = models.CharField(help_text="Short description for the product",max_length=200)
    tags = TaggableManager()

    objects = ProductManager()

    def all_images(self):
        images = self.images.all()
        images_url = [image.image.url for image in images]
        images_url = images_url.insert(0, self.image.url)

        return images_url

    class Meta:
        indexes = [
            models.Index(fields=["-created"]),
            models.Index(fields=["name", "slug"])
        ]
        ordering = ["-created", "-updated", "-id"]


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = generate_unique_slug(self, 'slug', 'name')
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=product_image_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"


class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="sizes")
    size = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Product Size"
        verbose_name_plural = "Product Sizes"


class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="colors")
    color = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Product Color"
        verbose_name_plural = "Product Colors"
