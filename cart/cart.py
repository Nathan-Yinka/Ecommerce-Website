from decimal import Decimal

from django.conf import settings

from shop.models import Product, ProductSize, ProductColor


class Cart:

    def __init__(self, request):
        """
        Initializes a new Cart
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
            self.cart = cart

    def add(self, product, quantity, override_quantity=False, size=None, color=None):
        """
        Add a product to the cart or update it quantity
        """
        variant_key = self._generate_variant_key(product, size, color)

        if variant_key not in self.cart:
            self.cart[variant_key] = {"quantity": 0}
        if override_quantity:
            self.cart[variant_key]["quantity"] = quantity
        else:
            self.cart[variant_key]["quantity"] += quantity

        self.save()

    def remove(self, product, size=None, color=None, remove_all=False):
        """
        Remove a product from the cart, either all quantities or just one.
        """
        variant_key = self._generate_variant_key(product, size, color)

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

        for item in cart.values():
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
        self.session.modified = True

    def clear(self):
        # remove the cart from the session
        self.cart = {}
        del self.session[settings.CART_SESSION_ID]
        self.save()

    @staticmethod
    def _generate_variant_key(product, size=None, color=None):
        """
        generate the variant key for a given product in
        the cart
        """
        product_id = str(product.id)
        size_id = str(size.id) if size else ""
        color_id = str(color.id) if color else ""
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
