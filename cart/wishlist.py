from django.conf import settings

from .models import Cart as WishlistModel

from shop.models import Product


class Wishlist:

    def __init__(self, request):
        """
                Initializes a new wishlist
        """
        self.session = request.session
        self.wishlist = self.initialize_wishlist(request)
        self.request = request

    def initialize_wishlist(self, request):
        wishlist_data = self.session.get(settings.WISHLIST_SESSION_ID, [])
        if request.user.is_authenticated:
            user_wishlist, created = WishlistModel.objects.get_or_create(user=request.user, type="wishlist")
            if len(wishlist_data) != 0:
                user_wishlist.data = wishlist_data.copy()
                user_wishlist.save()
                self.session[settings.WISHLIST_SESSION_ID] = []
                self.session.save()
            return user_wishlist.data.copy()
        else:
            return wishlist_data

    def add(self, product_id):
        """
            Add a product to the wishlist
        """
        product_id = str(product_id)
        if product_id not in self.wishlist:
            self.wishlist.append(product_id)
            self.save()

    def remove(self, product_id):
        """
        Remove a product from the wishlist
        """
        product_id = str(product_id)
        if product_id in self.wishlist:
            self.wishlist.remove(product_id)
            self.save()

    def clear(self):
        # remove the cart from the session
        self.wishlist = []
        self.save()

    def __iter__(self):
        """Iterate over the items in the wishlist and get the products
            from the database.
        """
        wishlist_id_int = [int(item) for item in set(self.wishlist)]
        products = Product.objects.filter(id__in=wishlist_id_int)

        for product in products:
            yield product

    def __len__(self):
        """Count the length of all the items in the cart
        """
        return len(set(self.wishlist))

    def save(self):
        """
        marks the sessions as modified to make sure it get saved
        """
        if self.request.user.is_authenticated:
            wishlist = self.request.user.cart.get(type='wishlist')
            wishlist.data = self.wishlist.copy()
            wishlist.save()
        else:
            self.session[settings.WISHLIST_SESSION_ID] = self.wishlist
            self.session.modified = True
