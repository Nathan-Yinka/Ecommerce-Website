from rest_framework import generics

from shop.models import Product


from .serializers import ProductSerializer

from myshop.pagination import ProductPageNumberPagination


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = ProductPageNumberPagination

    def get_queryset(self):
        query = self.request.GET.get('q', "")
        min_price = self.request.GET.get('min', None)
        max_price = self.request.GET.get('max', None)
        tags_str = self.request.GET.get('tags')
        colors_str = self.request.GET.get('colors')

        # Split tags and colors by comma
        tags = tags_str.split(',') if tags_str else []
        colors = colors_str.split(',') if colors_str else []

        queryset = super().get_queryset().search(query=query, min_price=min_price, max_price=max_price, tags=tags,
                                                 colors=colors)
        return queryset.available()
