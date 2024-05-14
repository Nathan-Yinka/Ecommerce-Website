from rest_framework import serializers
from shop.models import Product,ProductSize,ProductColor
from shop.api.serializers import ProductColorSerializer,ProductSizeSerializer


class CartAddProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def __init__(self, *args, **kwargs):
        product_id = kwargs.pop('product_id', None)
        super().__init__(*args, **kwargs)

        if product_id is not None:
            try:
                product = Product.objects.prefetch_related('sizes', 'colors').get(id=product_id)

                if product.sizes.exists():
                    self.fields['size_id'] = serializers.IntegerField(
                        required=True,
                        error_messages={'required': 'Please select a size for the product.'}
                    )

                if product.colors.exists():
                    self.fields['color_id'] = serializers.IntegerField(
                        required=True,
                        error_messages={'required': 'Please select a color for the product.'}
                    )

            except Product.DoesNotExist:
                raise serializers.ValidationError({'product_id': ["Invalid product."]})

    def validate(self, data):
        validated_data = super().validate(data)
        product_id = validated_data.get('product_id')
        size_id = validated_data.get('size_id')
        color_id = validated_data.get('color_id')

        if product_id is not None:
            try:
                product = Product.objects.prefetch_related('sizes', 'colors').get(id=product_id)

                if size_id is not None and not product.sizes.filter(id=size_id).exists():
                    raise serializers.ValidationError("Invalid size for the selected product.")

                if color_id is not None and not product.colors.filter(id=color_id).exists():
                    raise serializers.ValidationError("Invalid color for the selected product.")
            except Product.DoesNotExist:
                raise serializers.ValidationError("Invalid product.")

        return validated_data


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField()
    product = ProductSerializer()
    color = ProductColorSerializer(required=False, allow_null=True)
    size = ProductSizeSerializer(required=False, allow_null=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)


class CartDeleteSerializer(CartAddProductSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the 'quantity' field
        self.fields.pop('quantity', None)



