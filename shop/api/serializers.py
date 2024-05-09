from rest_framework import serializers
from taggit.serializers import TagListSerializerField


from shop.models import Product,ProductImage,ProductSize,ProductColor


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

    class Meta:
        model = Product
        fields = "__all__"
        depth = 1
