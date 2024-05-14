import random
import math

from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy
from django.db.models import Max
from taggit.models import Tag

from .models import Category, Product, ProductColor


# Create your views here.

class HomeView(ListView):
    model = Product
    template_name = "shop/product.html"
    context_object_name = "products"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        categories, random_categories = self.get_filter_category_list()

        context['categories'] = categories
        context['random_categories'] = random_categories

        context['prices'], context['max_price'] = self.get_filter_product_price()

        context['colors'] = self.get_filter_colour_list()

        context['tags'] = self.get_all_tags()
        context['page'] = "home"
        return context

    def get_filter_product_price(self):
        products = self.get_queryset()
        highest_price = products.aggregate(max_price=Max('price'))['max_price']
        if highest_price is not None:
            highest_price_rounded = math.ceil(highest_price / 100) * 100
            price_range = highest_price_rounded / 5
            price_ranges = [(i * price_range, (i + 1) * price_range) for i in range(5)]
            return price_ranges, highest_price_rounded
        return [], ""

    @staticmethod
    def get_filter_colour_list():
        product_colour = ProductColor.objects.all().distinct("color")
        colors = [color.color for color in product_colour][:10]
        return colors

    @staticmethod
    def get_filter_category_list():
        categories = Category.objects.all()
        categories_with_images = categories.filter(image__isnull=False)
        random_categories = list(categories_with_images)[:3]
        random.shuffle(random_categories)

        return categories, random_categories

    @staticmethod
    def get_all_tags():
        tags = Tag.objects.all()
        return tags


class ShopView(HomeView):

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page'] = "shop"
        context["shop_query"] = self.get_shop_query()

        return context

    def get_shop_query(self):
        category_slug = self.request.session.pop('category_slug', None)
        if category_slug:
            category = Category.objects.filter(slug=category_slug).first()
            return category
        return None


class CategoryRedirectView(RedirectView):
    url = reverse_lazy("shop:shop")

    def get_redirect_url(self, *args, **kwargs):
        category_slug = kwargs.get("category_slug", None)
        if category_slug:
            self.request.session['category_slug'] = category_slug
        return super().get_redirect_url(*args, **kwargs)
