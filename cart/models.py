from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

User = get_user_model()


def default_cart_data(type):
    if type == "cart":
        return {}
    else:
        return set()

cart_choices = [
    ("cart","cart"),
    ("wishlist","wishlist"),
]


class Cart(models.Model):
    user = models.ForeignKey(User, related_name="cart", on_delete=models.CASCADE, editable=False)
    data = models.JSONField(editable=False)
    type = models.CharField(max_length=100,choices=cart_choices,editable=False)

    def __str__(self):
        return f"{self.user.username} {self.type}"

    def save(self,*args,**kwargs):
        if not self.data:
            if self.type == "cart":
                self.data = {}
            else:
                self.data = []
        super().save(*args,**kwargs)

