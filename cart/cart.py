from decimal import Decimal

from django.conf import settings


from .models import Cart as CartModel
from shop.models import Product, ProductSize, ProductColor


class Cart:

    def __init__(self, request):
        """
        Initializes a new Cart
        """
        self.session = request.session
        self.cart = self.initialize_cart(request)
        self.request = request

    def initialize_cart(self, request):
        cart_data = self.session.get(settings.CART_SESSION_ID, {})
        if request.user.is_authenticated:
            user_cart, created = CartModel.objects.get_or_create(user=request.user)
            if len(cart_data) != 0:
                user_cart.data = cart_data.copy()
                user_cart.save()
                self.session[settings.CART_SESSION_ID] = {}
                self.session.save()
            return user_cart.data.copy()
        else:
            return cart_data

    def add(self, product_id, quantity, override_quantity=False, size_id=None, color_id=None):
        """
        Add a product to the cart or update it quantity
        """
        variant_key = self._generate_variant_key(product_id, size_id, color_id)

        if variant_key not in self.cart:
            self.cart[variant_key] = {"quantity": 0}
        if override_quantity:
            self.cart[variant_key]["quantity"] = quantity
        else:
            self.cart[variant_key]["quantity"] += quantity
        self.save()

    def remove(self, product_id, size_id=None, color_id=None, remove_all=False):
        """
        Remove a product from the cart, either all quantities or just one.
        """
        variant_key = self._generate_variant_key(product_id, size_id, color_id)

        if variant_key in self.cart:
            if remove_all:
                del self.cart[variant_key]
            else:
                self.cart[variant_key]["quantity"] -= 1
                if self.cart[variant_key]["quantity"] <= 0:
                    del self.cart[variant_key]
            self.save()

    def __iter__(self):
        """Iterate over the items in the cart and get the products
            from the database.
        """
        variant_keys = list(self.cart.keys())
        cart = {}
        for key in variant_keys:
            product_id, size_id, color_id = self._split_variant_key(key)
            try:
                product = Product.objects.prefetch_related("sizes", "colors").get(id=product_id)
                size = product.sizes.get(id=size_id) if size_id else None
                color = product.colors.get(id=color_id) if color_id else None
                cart[key] = {
                    "quantity": self.cart[key]["quantity"],
                    "product": product,
                    "color": color,
                    "size": size
                }
            except (Product.DoesNotExist, ProductSize.DoesNotExist, ProductColor.DoesNotExist):
                # Handle missing product, size, or color gracefully
                if key in cart:
                    del cart[key]
                if key in self.cart:
                    del self.cart[key]

        for item in sorted(cart.values(), key=lambda x: (x["product"].name)):
            item["price"] = Decimal(item["product"].price)
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """Count the length of all the items in the cart
        """
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        """
        get the total price for the cart
        """
        return sum(item["total_price"] for item in self)

    def save(self):
        """
        marks the sessions as modified to ake sure it get saved
        """
        if self.request.user.is_authenticated:
            cart = self.request.user.cart
            cart.data = self.cart.copy()
            cart.save()
        else:
            self.session[settings.CART_SESSION_ID] = self.cart
            self.session.modified = True

    def clear(self):
        # remove the cart from the session
        self.cart = {}
        self.save()

    @staticmethod
    def _generate_variant_key(product_id, size_id=None, color_id=None):
        """
        generate the variant key for a given product in
        the cart
        """
        product_id = str(product_id)
        size_id = str(size_id) if size_id else ""
        color_id = str(color_id) if color_id else ""
        return f"{product_id}-{size_id}-{color_id}"

    @staticmethod
    def _split_variant_key(variant_key):
        """
        Split the variant key into its components: product ID, size ID, and color ID.
        """
        parts = variant_key.split("-")
        product_id = int(parts[0])
        size_id = int(parts[1]) if len(parts) > 1 and parts[1] else None
        color_id = int(parts[2]) if len(parts) > 2 and parts[2] else None
        return product_id, size_id, color_id
