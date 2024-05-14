from django import forms
from django.shortcuts import get_object_or_404
from shop.models import Product


class CartAddProductForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(min_value=1)

    def __init__(self, *args, **kwargs):
        product_id = kwargs.pop('product_id', None)
        super().__init__(*args, **kwargs)

        if product_id is not None:
            try:
                product = Product.objects.prefetch_related('sizes', 'colors').get(id=product_id)

                if product.sizes.exists():
                    self.fields['size_id'] = forms.IntegerField(
                        required=True,
                        error_messages={'required': 'Please select a size for the product.'}
                    )

                if product.colors.exists():
                    self.fields['color_id'] = forms.IntegerField(
                        required=True,
                        error_messages={'required': 'Please select a color for the product.'}
                    )

            except Product.DoesNotExist:
                self.add_error(None, forms.ValidationError("Invalid product."))

    def clean(self):
        cleaned_data = super().clean()
        product_id = cleaned_data.get('product_id')
        size_id = cleaned_data.get('size_id')
        color_id = cleaned_data.get('color_id')

        try:
            product = Product.objects.prefetch_related('sizes', 'colors').get(id=product_id)

            if size_id is not None:
                size = product.sizes.filter(id=size_id).first()
                if size is None:
                    self.add_error('size_id', "Invalid size for the selected product.")

            if color_id is not None:
                color = product.colors.filter(id=color_id).first()
                if color is None:
                    self.add_error('color_id', "Invalid color for the selected product.")
        except Product.DoesNotExist:
            self.add_error(None, forms.ValidationError("Invalid product."))

        return cleaned_data
