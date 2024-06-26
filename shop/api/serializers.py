from rest_framework import serializers
from taggit.serializers import TagListSerializerField


from shop.models import Product,ProductImage,ProductSize,ProductColor
from cart.wishlist import Wishlist


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = ['id', 'size']


class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ['id', 'color']


class ProductSerializer(serializers.ModelSerializer):
    tags = TagListSerializerField()
    images = ProductImageSerializer(many=True)
    sizes = ProductSizeSerializer(many=True)
    colors = ProductColorSerializer(many=True)
    in_wishlist = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"
        depth = 1

    def get_in_wishlist(self, product):
        request = self.context['request']
        wishlist = Wishlist(request)
        if str(product.id) in wishlist.wishlist:
            return True
        return False
