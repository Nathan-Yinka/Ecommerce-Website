from decimal import Decimal

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory
from django.test import TestCase

from shop.models import Product, ProductSize, ProductColor, Category
from .cart import Cart
from .wishlist import Wishlist

User = get_user_model()


class CartTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.factory = RequestFactory()

        # Create a dummy image file for testing
        image_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x01\x03\x00\x00\x00\x1f'
        self.image = SimpleUploadedFile("test_image.png", image_content, content_type="image/png")

        # Create a category for testing
        self.category = Category.objects.create(name="Test Category")

        # Create a product for testing
        self.product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            category=self.category,
            price=Decimal('10.00'),
            available=True,
            description="This is a test product description.",
            image=self.image
        )

        # Create product sizes and colors for testing
        self.size1 = ProductSize.objects.create(product=self.product, size="Small")
        self.size2 = ProductSize.objects.create(product=self.product, size="Medium")

        self.color1 = ProductColor.objects.create(product=self.product, color="Red")
        self.color2 = ProductColor.objects.create(product=self.product, color="Blue")

    @property
    def request(self):
        request = self.factory.get('/')
        request.user = AnonymousUser()  # swap request with self.user and AnonymousUser() to test for authenticated
                                        # user annd Anonymous user

        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()

        return request

    def test_add_product_to_cart(self):
        # Initialize a cart and add a product
        cart = Cart(self.request)
        cart.add(self.product.id, quantity=2, size_id=self.size1.id, color_id=self.color1.id)

        # Check if the product is added to the cart correctly
        self.assertEqual(len(cart), 2)
        self.assertEqual(cart.get_total_price(), Decimal('20.00'))

    def test_add_product_with_different_sizes_and_colors_to_cart(self):
        # Initialize a cart
        cart = Cart(self.request)

        # Add products with different sizes and colors to the cart
        cart.add(self.product.id, quantity=1, size_id=self.size1.id, color_id=self.color1.id)
        cart.add(self.product.id, quantity=1, size_id=self.size1.id, color_id=self.color1.id)
        cart.add(self.product.id, quantity=1, size_id=self.size1.id, color_id=self.color1.id)
        cart.add(self.product.id, quantity=2, size_id=self.size2.id, color_id=self.color2.id)

        # Check if the products are added to the cart correctly
        self.assertEqual(len(cart), 5)  # Total quantity should be 3
        self.assertEqual(cart.get_total_price(), Decimal('50.00'))
        self.assertEqual(len(cart.cart.values()), 2)

    def test_remove_product_from_cart(self):
        # Initialize a cart and add a product
        cart = Cart(self.request)
        cart.add(self.product.id, quantity=3, size_id=self.size2.id, color_id=self.color2.id)

        # Remove one quantity of the product from the cart
        cart.remove(self.product.id, size_id=self.size2.id, color_id=self.color2.id)

        # Check if the quantity is updated correctly
        self.assertEqual(len(cart), 2)

    def test_remove_all_product_instances_from_cart(self):
        # Initialize a cart and add a product
        cart = Cart(self.request)
        cart.add(self.product.id, quantity=3, size_id=self.size2.id, color_id=self.color2.id)

        # Remove all instances of the product from the cart
        cart.remove(self.product.id, size_id=self.size2.id, color_id=self.color2.id, remove_all=True)

        # Check if the product is completely removed from the cart
        self.assertEqual(len(cart), 0)

    def test_iterate_over_cart_items(self):
        # Initialize a cart
        cart = Cart(self.request)

        # Add products to the cart
        cart.add(self.product.id, quantity=2, size_id=self.size1.id, color_id=self.color1.id)
        cart.add(self.product.id, quantity=1, size_id=self.size2.id, color_id=self.color2.id)

        # delete the size from the database
        self.size1.delete()
        # update the price of the product
        self.product.price = 20
        self.product.save()

        # Iterate over the cart items
        for item in cart:
            # Check if the required keys exist in the item dictionary
            self.assertIn("quantity", item)
            self.assertIn("product", item)
            self.assertIn("color", item)
            self.assertIn("size", item)
            self.assertIn("price", item)
            self.assertIn("total_price", item)

            # Check if the product object is an instance of Product model
            self.assertIsInstance(item["product"], Product)

            # Check if the price and total_price are calculated correctly
            self.assertEqual(item["price"], Decimal('20.00'))  # product have been updated to 20
            self.assertEqual(item["total_price"], item['price'] * item['quantity'])

        # Check if the total number of items in the cart is correct
        self.assertEqual(len(cart),
                         1)  # Total quantity should be 1 since the size has been deleted from the database and the
        # cart entry for that product will  be deleted from the cart

    def test_clear_cart(self):
        # Initialize a cart and add some products
        cart = Cart(self.request)
        cart.add(self.product.id, quantity=2, size_id=self.size1.id, color_id=self.color1.id)
        cart.add(self.product.id, quantity=1, size_id=self.size2.id, color_id=self.color2.id)

        # Check if the cart is not empty before clearing
        self.assertGreater(len(cart), 0)

        # Clear the cart
        cart.clear()

        # Check if the cart is empty after clearing
        self.assertEqual(len(cart), 0)

        # Check if the cart has been removed from the session
        self.assertNotIn(settings.CART_SESSION_ID, self.client.session)

    def test_generate_variant_key(self):
        # Call the _generate_variant_key method with the product, size, and color
        variant_key = Cart._generate_variant_key(self.product.id, size_id=self.size1.id, color_id=self.color1.id)
        variant_key2 = Cart._generate_variant_key(self.product.id, size_id=None, color_id=self.color1.id)
        variant_key3 = Cart._generate_variant_key(self.product.id, size_id=self.size1.id, color_id=None)
        variant_key4 = Cart._generate_variant_key(self.product.id, size_id=None, color_id=None)

        # Expected variant key format: "<product_id>-<size_id>-<color_id>"
        expected_key = f"{self.product.id}-{self.size1.id}-{self.color1.id}"
        expected_key2 = f"{self.product.id}--{self.color1.id}"
        expected_key3 = f"{self.product.id}-{self.size1.id}-"
        expected_key4 = f"{self.product.id}--"

        # Assert whether the generated variant key matches the expected key
        self.assertEqual(variant_key, expected_key)
        self.assertEqual(variant_key2, expected_key2)
        self.assertEqual(variant_key3, expected_key3)
        self.assertEqual(variant_key4, expected_key4)

    def test_split_variant_key(self):
        # Sample variant key format: "<product_id>-<size_id>-<color_id>"
        variant_key = "1-2-3"  # Example variant key

        # Call the _split_variant_key method with the sample variant key
        product_id, size_id, color_id = Cart._split_variant_key(variant_key)

        # Expected component values
        expected_product_id = 1
        expected_size_id = 2
        expected_color_id = 3

        # Assert whether the returned component values match the expected values
        self.assertEqual(product_id, expected_product_id)
        self.assertEqual(size_id, expected_size_id)
        self.assertEqual(color_id, expected_color_id)


class WishlistTestCase(TestCase):
    def setUp(self):
        # Create a user for testing
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='12345')

        # Create some products for testing
        self.category = Category.objects.create(name="Test Category")
        image_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x01\x03\x00\x00\x00\x1f'
        self.image = SimpleUploadedFile("test_image.png", image_content, content_type="image/png")
        self.product1 = Product.objects.create(
            name="Test Product1",
            slug="test-product1",
            category=self.category,
            price=Decimal('10.00'),
            available=True,
            description="This is a test product description.",
            image=self.image
        )
        self.product2 = Product.objects.create(
            name="Test Product2",
            slug="test-product2",
            category=self.category,
            price=Decimal('10.00'),
            available=True,
            description="This is a test product description.",
            image=self.image
        )

    @property
    def request(self):
        request = self.factory.get('/')
        request.user = AnonymousUser()  # swap request with self.user and AnonymousUser() to test for authenticated
        # user and Anonymous user

        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()

        return request

    def test_add_to_wishlist(self):
        # Initialize wishlist for the user
        request = self.request
        wishlist = Wishlist(request)

        # Add a product to the wishlist
        wishlist.add_or_remove(self.product1.id)
        # adding the same product to the wishlist
        wishlist.add_or_remove(self.product1.id)
        wishlist.add_or_remove(self.product1.id)

        # Check if the product is added to the wishlist
        self.assertIn(str(self.product1.id), wishlist.wishlist)
        self.assertEqual(len(wishlist),1)


    def test_wishlist_iteration_and_length(self):
        # Iterate over the wishlist
        request = self.request
        wishlist = Wishlist(request)

        # Add a product to the wishlist
        wishlist.add_or_remove(self.product1.id)
        wishlist.add_or_remove(self.product2.id)

        products_in_wishlist = list(wishlist)

        # Check if the correct products are returned
        self.assertEqual(len(products_in_wishlist), 2)
        self.assertIn(self.product1, products_in_wishlist)
        self.assertIn(self.product2, products_in_wishlist)